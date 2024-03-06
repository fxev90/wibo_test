import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../auth/auth.service';
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

  constructor(private http: HttpClient , private authService: AuthService) {}

  submitForm() {
    const formData = {
      username: this.username,
      password: this.password,
    };

    this.http.post<{access_token: string, token_type: string}>('http://127.0.0.1:8000/login', formData)
      .subscribe(response => {
        this.authService.login();
        this.authService.setToken(response['access_token']);
      }, error => {
        // Handle errors
        console.error(error);
      });
  }
}