import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';
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

  constructor(private http: HttpClient, private authService: AuthService, private router: Router) { }


  redirectToSignUp() {
    this.router.navigate(['/register']);
  }


  submitForm() {
    const formData = {
      username: this.username,
      password: this.password,
    };

    this.http.post<{ access_token: string, token_type: string }>('http://127.0.0.1:8000/login', formData)
      .subscribe(response => {
        this.authService.storage.setToken(response.access_token);
        this.router.navigate(['/users']);
      }, error => {
        // Handle errors
        console.error(error);
      });
  }
}