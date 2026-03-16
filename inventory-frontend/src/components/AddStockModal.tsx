import { FormEvent, useState } from 'react'

type Props = {
  loading: boolean
  initialName?: string
  onClose: () => void
  onSubmit: (name: string, quantity: number) => Promise<void>
}

export function AddStockModal({ loading, initialName = '', onClose, onSubmit }: Props) {
  const [name, setName] = useState(initialName)
  const [quantity, setQuantity] = useState(1)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    try {
      await onSubmit(name.trim(), quantity)
      onClose()
    } catch {
      // error handled in parent
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Adicionar ao estoque</h2>
          <button type="button" className="btn-icon" onClick={onClose} aria-label="Fechar">✕</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <label>
              <span>Nome do item</span>
              <input
                type="text"
                placeholder="Ex: Camiseta P"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                autoFocus
              />
            </label>
            <label>
              <span>Quantidade</span>
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
            <button type="submit" disabled={loading || !name.trim() || quantity < 1}>
              {loading ? 'Salvando...' : 'Adicionar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
