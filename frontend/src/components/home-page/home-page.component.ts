import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";
import { WorkingDaysValidator } from "src/utils";

@Component({
  selector: "app-home-page",
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: "./home-page.component.html",
  styleUrl: "./home-page.component.css"
})
export class HomePageComponent {
  submitted: boolean = false;
  INITIAL_NUMBER_OF_WORKING_DAYS = 22;
  MIN_NUMBER_OF_WORKING_DAYS = 12;
  MAX_NUMBER_OF_WORKING_DAYS = 24;
  loading = false;

  form = new FormGroup({
    fileInput: new FormControl("", [Validators.required]),
    key: new FormControl("", [Validators.required]),
    numberOfWorkingDays: new FormControl(this.INITIAL_NUMBER_OF_WORKING_DAYS, [
      Validators.required,
      WorkingDaysValidator(
        this.MIN_NUMBER_OF_WORKING_DAYS,
        this.MAX_NUMBER_OF_WORKING_DAYS
      )
    ])
  });

  generateSchedule() {
    console.log("Generate Schedule");
    console.log(this.form.value);
    this.submitted = true;
    if (this.form.invalid) {
      return;
    }
    this.loading = true;
    this.disableFormInputs();

    setTimeout(() => {
      this.loading = false;
      this.enableFormInputs();
    }, 2000);
  }

  disableFormInputs() {
    this.form.get("numberOfWorkingDays")?.disable();
    this.form.get("fileInput")?.disable();
    this.form.get("key")?.disable();
  }

  enableFormInputs() {
    this.form.get("numberOfWorkingDays")?.enable();
    this.form.get("fileInput")?.enable();
    this.form.get("key")?.enable();
  }
}
