import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  name: string = '';
  username: string = '';
  password: string = '';

  constructor(private http: HttpClient) {}

  submitForm() {
    const formData = {
      username: this.username,
      password: this.password,
    };

    // Assuming you have a backend server running at 127.0.0.1:8000
    this.http.post('http://127.0.0.1:8000/login', formData)
      .subscribe(response => {
        // Handle the response as needed
        console.log(response);
      }, error => {
        // Handle errors
        console.error(error);
      });
  }
}