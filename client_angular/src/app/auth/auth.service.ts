import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { tap, delay } from 'rxjs/operators';



const storagePrefix = 'wibo_';


@Injectable({
  providedIn: 'root',
})
export class AuthService {
  storage = {
    getToken: () => {
      return JSON.parse(window.localStorage.getItem(`${storagePrefix}token`) as string);
    },
    setToken: (token: string) => {
      window.localStorage.setItem(`${storagePrefix}token`, JSON.stringify(token));
    },
    clearToken: () => {
      window.localStorage.removeItem(`${storagePrefix}token`);
    },
  };
  isLoggedIn = false;
  // store the URL so we can redirect after logging in
  redirectUrl: string | null = "127.0.0.1:4200/users";

  login(): Observable<boolean> {
    return of(true).pipe(
      delay(500),
      tap(() => (this.isLoggedIn = true))
    );
  }

  logout(): void {
    this.isLoggedIn = false;
  }

  headers() {
    return { headers: { 'Authorization': `Bearer ${this.storage.getToken()}` } }
  }
}