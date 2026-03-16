import type { HealthStatus, InventoryItem } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const INVENTORY_BASE = `${API_BASE_URL}/api/inventory`
const HEALTH_URL = `${API_BASE_URL}/health/`

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = 'Erro inesperado ao comunicar com a API.'

    try {
      const payload = (await response.json()) as { detail?: string }
      if (payload?.detail) detail = payload.detail
    } catch {
      // ignore json parse errors
    }

    throw new Error(detail)
  }

  return (await response.json()) as T
}

export async function getHealth(): Promise<HealthStatus> {
  const response = await fetch(HEALTH_URL)
  return handleResponse<HealthStatus>(response)
}

export async function listInventory(orderBy?: string, direction?: string): Promise<InventoryItem[]> {
  const params = new URLSearchParams()
  if (orderBy) params.set('order_by', orderBy)
  if (direction) params.set('direction', direction)

  const qs = params.toString()
  const response = await fetch(`${INVENTORY_BASE}/${qs ? `?${qs}` : ''}`)
  return handleResponse<InventoryItem[]>(response)
}

export async function addStock(name: string, quantity: number): Promise<InventoryItem> {
  const response = await fetch(`${INVENTORY_BASE}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, quantity }),
  })
  return handleResponse<InventoryItem>(response)
}

export async function removeStock(itemId: string, quantity: number): Promise<InventoryItem> {
  const response = await fetch(`${INVENTORY_BASE}/${itemId}/`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quantity }),
  })
  return handleResponse<InventoryItem>(response)
}
