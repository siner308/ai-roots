import { useState, useEffect } from "react";

/**
 * Delays propagating `value` to consumers until `delayMs` milliseconds have
 * elapsed since the last change.  Cleans up its timeout on unmount and
 * restarts the timer whenever `delayMs` itself changes.
 *
 * @param value   - The value to debounce.
 * @param delayMs - How long to wait (ms) after the last change before updating.
 * @returns The debounced value.
 */
function useDebouncedValue<T>(value: T, delayMs: number): T {
  // Initialize with the current value so the first render is not stale.
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    // Schedule the update after the specified delay.
    const timerId = setTimeout(() => {
      setDebouncedValue(value);
    }, delayMs);

    // Cancel the pending timeout if:
    //   - `value` changes before the delay expires (resets the timer), or
    //   - `delayMs` changes (restarts with the new delay), or
    //   - the component unmounts (prevents a state update on an unmounted component).
    return () => {
      clearTimeout(timerId);
    };
  }, [value, delayMs]);

  return debouncedValue;
}

export default useDebouncedValue;
