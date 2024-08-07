import { AbstractControl, ValidatorFn, ValidationErrors } from "@angular/forms";

export function WorkingDaysValidator(min: number, max: number): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    if (!control.value) {
      return null;
    }

    const valueStr = control.value.toString();
    const numberPattern = /^\d+$/;

    // Check if the value matches the regex pattern
    if (!numberPattern.test(valueStr)) {
      return { numericError: "The input must contain only numbers" };
    }

    const value = parseInt(valueStr, 10);

    // Check if the value is within the specified range
    if (isNaN(value) || value < min || value > max) {
      return { rangeError: `Value must be between ${min} and ${max}` };
    }

    return null;
  };
}
