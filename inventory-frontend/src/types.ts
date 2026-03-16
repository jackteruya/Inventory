export type InventoryItem = {
  id: string
  name: string
  quantity: number
  last_updated: string
}

export type HealthStatus = {
  status: 'ok' | 'degraded'
  database: boolean
  rabbitmq: boolean
}
