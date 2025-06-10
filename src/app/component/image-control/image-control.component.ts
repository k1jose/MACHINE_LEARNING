import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-image-control',
  imports: [CommonModule],
  templateUrl: './image-control.component.html',
  styleUrl: './image-control.component.scss',
})
export class ImageControlComponent {
  imageUrl: string | null = null;
  selectedFile: File | null = null;
  // Arreglo de predicciones individuales
  detections: { class: string; score: number }[] = [];
  isLoading = false;

  private http = inject(HttpClient);

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.selectedFile = input.files[0];

      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        this.imageUrl = e.target?.result as string;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  onUpload() {
    if (!this.selectedFile) return;

    this.isLoading = true;
    this.detections = [];

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<any>('http://localhost:8000/predict', formData).subscribe({
      next: (res) => {
        this.detections = res.classes.map((cls: string, i: number) => ({
          class: cls,
          score: res.scores[i],
        }));
        this.isLoading = false;
      },
      error: () => {
        alert('Error al subir la imagen.');
        this.isLoading = false;
      },
    });
  }
}
