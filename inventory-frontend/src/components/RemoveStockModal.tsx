import { FormEvent, useState } from 'react'
import type { InventoryItem } from '../types'

type Props = {
  items: InventoryItem[]
  loading: boolean
  initialItemId?: string
  onClose: () => void
  onSubmit: (itemId: string, quantity: number) => Promise<void>
}

export function RemoveStockModal({ items, loading, initialItemId, onClose, onSubmit }: Props) {
  const [selectedId, setSelectedId] = useState(initialItemId ?? items[0]?.id ?? '')
  const [quantity, setQuantity] = useState(1)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!selectedId) return
    try {
      await onSubmit(selectedId, quantity)
      onClose()
    } catch {
      // error handled in parent
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Remover do estoque</h2>
          <button type="button" className="btn-icon" onClick={onClose} aria-label="Fechar">✕</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <label>
              <span>Item</span>
              <select
                value={selectedId}
                onChange={(e) => setSelectedId(e.target.value)}
                required
              >
                {items.length === 0 ? (
                  <option value="">Nenhum item disponível</option>
                ) : (
                  items.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.name} — {item.quantity} un.
                    </option>
                  ))
                )}
              </select>
            </label>
            <label>
              <span>Quantidade a remover</span>
              <input
                type="number"
                min={1}
                value={quantity}
                onChange={(e) => setQuantity(Number(e.target.value))}
                required
              />
            </label>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose}>Cancelar</button>
            <button
              type="submit"
              className="btn-danger"
              disabled={loading || !selectedId || quantity < 1}
            >
              {loading ? 'Removendo...' : 'Remover'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
