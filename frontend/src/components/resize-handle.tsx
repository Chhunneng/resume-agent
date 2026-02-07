import { forwardRef } from "react"
import { GripVertical } from "lucide-react"

interface ResizeHandleProps {
  onResizeStart: (e: React.PointerEvent) => void
}

export const ResizeHandle = forwardRef<HTMLButtonElement, ResizeHandleProps>(
  function ResizeHandle({ onResizeStart }, ref) {
    return (
      <button
        ref={ref}
        type="button"
        aria-label="Resize panels"
        className="group touch-none flex w-4 shrink-0 cursor-col-resize items-center justify-center rounded-full border-0 bg-transparent outline-none transition-[background-color,box-shadow] duration-200 hover:bg-muted/50 hover:shadow-inner focus:ring-2 focus:ring-primary/40 focus:ring-offset-2 focus:ring-offset-background active:bg-muted/60 md:w-5"
        onPointerDown={onResizeStart}
      >
        <GripVertical
          className="size-4 text-muted-foreground/50 transition-colors duration-200 group-hover:text-muted-foreground md:size-5"
          strokeWidth={2}
          aria-hidden
        />
      </button>
    )
  }
)
