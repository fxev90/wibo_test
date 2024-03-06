import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { tap, delay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isLoggedIn = false;
  token: string | null = null;
  // store the URL so we can redirect after logging in
  redirectUrl: string | null = "127.0.0.1:8000/users/";

  login(): Observable<boolean> {
    return of(true).pipe(
      delay(500),
      tap(() => (this.isLoggedIn = true))
    );
  }

  logout(): void {
    this.isLoggedIn = false;
  }

  setToken(token: string): void {
    this.token = token;
  }
  getToken(): string | null {
    return this.token;
  }
}