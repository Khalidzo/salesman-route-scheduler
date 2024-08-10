import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";
import { Observable, map } from "rxjs";
import {
  GoogleMap,
  GoogleMapsModule,
  MapDirectionsRenderer,
  MapDirectionsService
} from "@angular/google-maps";
import { WorkingDaysValidator } from "src/utils";

@Component({
  selector: "app-home-page",
  standalone: true,
  imports: [
    ReactiveFormsModule,
    CommonModule,
    GoogleMap,
    GoogleMapsModule,
    MapDirectionsRenderer
  ],
  templateUrl: "./home-page.component.html",
  styleUrl: "./home-page.component.css"
})
export class HomePageComponent {
  submitted: boolean = false;
  INITIAL_NUMBER_OF_WORKING_DAYS = 22;
  MIN_NUMBER_OF_WORKING_DAYS = 12;
  MAX_NUMBER_OF_WORKING_DAYS = 24;
  loading = false;
  activeBtnIndex = 0;
  arrayTen = Array.from({ length: 11 }, (_, i) => i + 1);

  readonly directionsResults$: Observable<
    google.maps.DirectionsResult | undefined
  >;

  constructor(mapDirectionsService: MapDirectionsService) {
    const request: google.maps.DirectionsRequest = {
      destination: { placeId: "ChIJz3_MbfRDXz4Rx9PsK0czlcE" },
      waypoints: [{ location: { placeId: "ChIJd6MbiE5pXz4R6KGOoL1Pxtc" } }],
      origin: { lat: 25.2030864, lng: 55.2781753 },
      travelMode: "DRIVING" as google.maps.TravelMode
    };

    this.directionsResults$ = mapDirectionsService
      .route(request)
      .pipe(map((response) => response.result));
  }

  // Example of a Google Map markers
  locations: google.maps.LatLngLiteral[] = [
    { lat: 25.1581958, lng: 55.25932 },
    { lat: 25.2030864, lng: 55.2781753 },
    { lat: 25.2105107, lng: 55.282596 }
  ];

  // Maps props
  center: google.maps.LatLngLiteral = { lat: 25.206987, lng: 55.296249 };
  zoom = 12.6;
  options: google.maps.MapOptions = {
    center: this.center,
    streetViewControl: false, // Disable Street View
    mapTypeControl: false, // Disable Map Type Control
    fullscreenControl: false, // Disable Fullscreen Control
    draggableCursor: "default", // Change cursor to default
    zoomControl: false
  };

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

  setBtnActive(index: number) {
    this.activeBtnIndex = index;
  }
}
