export type TValidateParamsField<T extends unknown> = {
  /**
   * Лист функций-валидаторов.
   * True - валидатор прошел, false - валидатор не прошел.
   */
  validators: ((value: T) => boolean)[];
  /**
   * Стандартное значение или его геттер.
   * Если предоставлено, то декоратор не будет 
   * выбрасывать ошибку/возвращать общее стандартное значение.
   */
  defaultValue?: T | ((value?: T) => T);
}

export type TValidateParams<T extends unknown[]> = {
  /**
   * Описание параметров функции, к которй применяется декоратор
   */
  fields: {
    [K in keyof T]: TValidateParamsField<T[K]>;
  };
  /**
   * Общие опции декоратора
   */
  options?: {
    throw?: boolean;
    throws?: Error | (() => Error);
    return?: boolean;
    returns?: unknown | (() => unknown);
  };
};

export type TTypedFunction<T extends unknown[], R extends unknown> = (
  ...args: { [K in keyof T]: T[K] }
) => R;

/**
 * Decorator for function parameters validation
 * @param [key: string] parameter name
 * @param [validators: ValidatorFn[]] array of validators
 */
export const validate = <T extends unknown[], R extends unknown>(
  params: TValidateParams<T>
) => {
  return (
    target: Object,
    propertyKey: string | symbol,
    descriptor: TypedPropertyDescriptor<TTypedFunction<T, R>>
  ): TypedPropertyDescriptor<TTypedFunction<T, R>> => {
    const originalHandler = descriptor.value;
    descriptor.value = function (...args: T) {
      for (const key in args) {
        
        const _defaultValue = params.fields[key].defaultValue;
        const _validators = params.fields[key].validators;

        /**
         * Флаг ошибки.
         * Принимает значение true, если валидатор не прошел и нет значения по умолчанию
         */
        let isError: boolean = false;

        for (const validator of _validators) {
          if (!validator({ value: args[key] })) {
            if (_defaultValue) {
              args[key] = typeof _defaultValue === 'function' ? _defaultValue(args[key]) : _defaultValue;
              break;
            }
            isError = true;
            break;
          }
        }

        if (isError) {
          
        }
      }
    };
    return descriptor;
  };
};
