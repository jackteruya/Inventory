import type { InventoryItem } from '../types'

type InventoryTableProps = {
  items: InventoryItem[]
  loading: boolean
  orderBy: string
  direction: string
  onOrderByChange: (value: string) => void
  onDirectionChange: (value: string) => void
  onAddItem: (item: InventoryItem) => void
  onRemoveItem: (item: InventoryItem) => void
}

function formatDate(value: string) {
  return new Date(value).toLocaleString('pt-BR')
}

export function InventoryTable({
  items,
  loading,
  orderBy,
  direction,
  onOrderByChange,
  onDirectionChange,
  onAddItem,
  onRemoveItem,
}: InventoryTableProps) {
  return (
    <section className="panel">
      <div className="panel-header inventory-header">
        <div>
          <h2>Itens em estoque</h2>
          <p>Visualize e ordene o inventário em tempo real.</p>
        </div>

        <div className="filters">
          <label>
            <span>Ordenar por</span>
            <select value={orderBy} onChange={(event) => onOrderByChange(event.target.value)}>
              <option value="">Padrão</option>
              <option value="name">Nome</option>
              <option value="quantity">Quantidade</option>
              <option value="last_updated">Última atualização</option>
            </select>
          </label>

          <label>
            <span>Direção</span>
            <select value={direction} onChange={(event) => onDirectionChange(event.target.value)}>
              <option value="">Padrão</option>
              <option value="asc">Ascendente</option>
              <option value="desc">Descendente</option>
            </select>
          </label>
        </div>
      </div>

      <div className="table-wrapper">
        {loading ? (
          <p className="empty-state">Carregando itens...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Quantidade</th>
                <th>Última atualização</th>
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan={4} className="empty-state">Nenhum item encontrado.</td>
                </tr>
              ) : null}

              {items.map((item) => (
                <tr key={item.id}>
                  <td>
                    <div className="item-name-cell">
                      <strong>{item.name}</strong>
                      {item.quantity < 5 ? <span className="low-stock">Estoque crítico</span> : null}
                    </div>
                  </td>
                  <td>{item.quantity}</td>
                  <td>{formatDate(item.last_updated)}</td>
                  <td>
                    <div className="row-actions">
                      <button type="button" className="btn-row-add" onClick={() => onAddItem(item)}>+ Adicionar</button>
                      <button type="button" className="btn-row-remove" onClick={() => onRemoveItem(item)}>− Remover</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  )
}
