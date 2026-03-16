import { useCallback, useEffect, useMemo, useState } from 'react'
import { addStock, getHealth, listInventory, removeStock } from './api'
import { AddStockModal } from './components/AddStockModal'
import { RemoveStockModal } from './components/RemoveStockModal'
import { InventoryTable } from './components/InventoryTable'
import { StatusBadge } from './components/StatusBadge'
import type { HealthStatus, InventoryItem } from './types'

const DEFAULT_ERROR = 'Não foi possível concluir a operação.'

export default function App() {
  const [items, setItems] = useState<InventoryItem[]>([])
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [loadingItems, setLoadingItems] = useState(true)
  const [addingItem, setAddingItem] = useState(false)
  const [removingItem, setRemovingItem] = useState(false)
  const [banner, setBanner] = useState<{ kind: 'success' | 'error'; text: string } | null>(null)
  const [orderBy, setOrderBy] = useState('')
  const [direction, setDirection] = useState('')
  const [addModalOpen, setAddModalOpen] = useState(false)
  const [removeModalOpen, setRemoveModalOpen] = useState(false)
  const [selectedItem, setSelectedItem] = useState<InventoryItem | null>(null)

  const totals = useMemo(() => {
    const totalItems = items.length
    const totalUnits = items.reduce((sum, item) => sum + item.quantity, 0)
    const criticalItems = items.filter((item) => item.quantity < 5).length
    return { totalItems, totalUnits, criticalItems }
  }, [items])

  const loadHealth = useCallback(async () => {
    try {
      const response = await getHealth()
      setHealth(response)
    } catch {
      setHealth(null)
    }
  }, [])

  const loadItems = useCallback(async () => {
    setLoadingItems(true)
    try {
      const response = await listInventory(orderBy || undefined, direction || undefined)
      setItems(response)
    } catch (error) {
      const message = error instanceof Error ? error.message : DEFAULT_ERROR
      setBanner({ kind: 'error', text: message })
    } finally {
      setLoadingItems(false)
    }
  }, [direction, orderBy])

  useEffect(() => {
    void loadHealth()
  }, [loadHealth])

  useEffect(() => {
    void loadItems()
  }, [loadItems])

  async function handleAddStock(name: string, quantity: number) {
    setBanner(null)
    setAddingItem(true)
    try {
      await addStock(name, quantity)
      setBanner({ kind: 'success', text: 'Estoque atualizado com sucesso.' })
      await Promise.all([loadItems(), loadHealth()])
    } catch (error) {
      const message = error instanceof Error ? error.message : DEFAULT_ERROR
      setBanner({ kind: 'error', text: message })
      throw error
    } finally {
      setAddingItem(false)
    }
  }

  async function handleRemoveStock(itemId: string, quantity: number) {
    setBanner(null)
    setRemovingItem(true)
    try {
      await removeStock(itemId, quantity)
      setBanner({ kind: 'success', text: 'Baixa de estoque realizada com sucesso.' })
      await Promise.all([loadItems(), loadHealth()])
    } catch (error) {
      const message = error instanceof Error ? error.message : DEFAULT_ERROR
      setBanner({ kind: 'error', text: message })
      throw error
    } finally {
      setRemovingItem(false)
    }
  }

  return (
    <main className="layout">
      <section className="hero panel">
        <div>
          <p className="eyebrow">Inventory Dashboard</p>
          <h1>Gestão de Estoque</h1>
          <p className="hero-copy">
            Consulte, adicione e remova itens do inventário em tempo real.
          </p>
        </div>

        <div className="status-row">
          <StatusBadge label={health?.status === 'ok' ? 'API saudável' : 'API degradada'} ok={health?.status === 'ok'} />
          <StatusBadge label={health?.database ? 'Banco OK' : 'Banco indisponível'} ok={Boolean(health?.database)} />
          <StatusBadge label={health?.rabbitmq ? 'RabbitMQ OK' : 'RabbitMQ indisponível'} ok={Boolean(health?.rabbitmq)} />
        </div>
      </section>

      <section className="metrics-grid">
        <article className="metric-card panel">
          <span>Total de itens</span>
          <strong>{totals.totalItems}</strong>
        </article>
        <article className="metric-card panel">
          <span>Total de unidades</span>
          <strong>{totals.totalUnits}</strong>
        </article>
        <article className="metric-card panel">
          <span>Itens críticos</span>
          <strong>{totals.criticalItems}</strong>
        </article>
      </section>

      {banner ? <div className={`banner ${banner.kind}`}>{banner.text}</div> : null}

      <div className="action-bar">
        <button type="button" onClick={() => setAddModalOpen(true)}>+ Adicionar item</button>
        <button type="button" className="btn-danger" onClick={() => setRemoveModalOpen(true)}>− Remover item</button>
      </div>

      <InventoryTable
        items={items}
        loading={loadingItems}
        orderBy={orderBy}
        direction={direction}
        onOrderByChange={setOrderBy}
        onDirectionChange={setDirection}
        onAddItem={(item) => { setSelectedItem(item); setAddModalOpen(true) }}
        onRemoveItem={(item) => { setSelectedItem(item); setRemoveModalOpen(true) }}
      />

      {addModalOpen && (
        <AddStockModal
          loading={addingItem}
          initialName={selectedItem?.name}
          onClose={() => { setAddModalOpen(false); setSelectedItem(null) }}
          onSubmit={handleAddStock}
        />
      )}

      {removeModalOpen && (
        <RemoveStockModal
          items={items}
          loading={removingItem}
          initialItemId={selectedItem?.id}
          onClose={() => { setRemoveModalOpen(false); setSelectedItem(null) }}
          onSubmit={handleRemoveStock}
        />
      )}
    </main>
  )
}
