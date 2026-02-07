import { useCallback, useRef, useState } from "react"

export interface UseResizePanelOptions {
  minPx?: number
  maxPercent?: number
  defaultPx?: number
}

export function useResizePanel(options: UseResizePanelOptions = {}) {
  const {
    minPx = 240,
    maxPercent = 0.85,
    defaultPx = 420,
  } = options

  const [leftPanelPx, setLeftPanelPx] = useState(defaultPx)
  const panelContainerRef = useRef<HTMLDivElement>(null)
  const resizeHandleRef = useRef<HTMLButtonElement>(null)
  const dragRef = useRef({ startX: 0, startW: 0 })
  const rafRef = useRef<number | null>(null)

  const handleResizeStart = useCallback(
    (e: React.PointerEvent) => {
      e.preventDefault()
      const handle = resizeHandleRef.current
      if (!handle) return
      handle.setPointerCapture(e.pointerId)
      dragRef.current = { startX: e.clientX, startW: leftPanelPx }
      document.body.style.cursor = "col-resize"
      document.body.style.userSelect = "none"

      const onMove = (moveEvent: PointerEvent) => {
        const delta = moveEvent.clientX - dragRef.current.startX
        const next = dragRef.current.startW + delta
        const el = panelContainerRef.current
        const maxPx = el ? el.getBoundingClientRect().width * maxPercent : 1200
        const clamped = Math.min(maxPx, Math.max(minPx, next))
        if (rafRef.current !== null) cancelAnimationFrame(rafRef.current)
        rafRef.current = requestAnimationFrame(() => {
          rafRef.current = null
          setLeftPanelPx(clamped)
        })
      }
      const onUp = () => {
        handle.releasePointerCapture(e.pointerId)
        handle.removeEventListener("pointermove", onMove)
        handle.removeEventListener("pointerup", onUp)
        handle.removeEventListener("pointercancel", onUp)
        document.body.style.cursor = ""
        document.body.style.userSelect = ""
        if (rafRef.current !== null) cancelAnimationFrame(rafRef.current)
      }
      handle.addEventListener("pointermove", onMove)
      handle.addEventListener("pointerup", onUp)
      handle.addEventListener("pointercancel", onUp)
    },
    [leftPanelPx, minPx, maxPercent]
  )

  return {
    leftPanelPx,
    setLeftPanelPx,
    panelContainerRef,
    resizeHandleRef,
    handleResizeStart,
  }
}
