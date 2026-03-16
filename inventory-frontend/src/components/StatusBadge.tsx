type StatusBadgeProps = {
  label: string
  ok: boolean
}

export function StatusBadge({ label, ok }: StatusBadgeProps) {
  return (
    <span className={`status-badge ${ok ? 'ok' : 'error'}`}>
      <span className="status-dot" />
      {label}
    </span>
  )
}
