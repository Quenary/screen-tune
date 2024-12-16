/**
 * This decorator prevents methods execution
 * pywebview is missing in global object.
 * @param fallback optional fallback function.
 * @returns target return / fallback return.
 */
export function isPywebview(fallback?: Function) {
  return function isPywebview(
    target: Object,
    propertyKey: string,
    descriptor: any
  ) {
    const original = descriptor.value;
    descriptor.value = function (...args: any[]) {
      if (!window?.pywebview?.api) {
        console.warn(
          `${this?.constructor?.name}[${propertyKey}] decorated with @isPywebview cannot be called because electron is missing in global object.`
        );
        return !!fallback ? fallback(args) : null;
      }
      return original.apply(this, args);
    };
    return descriptor;
  };
}
