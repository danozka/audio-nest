import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { map, tap, catchError } from 'rxjs/operators';
import { Router } from '@angular/router';
import { ApiError} from '../models/api-error.model';
import { AuthResponse} from '../models/auth-response.model';
import { LoginRequest } from '../models/login-request.model';
import { RegisterRequest } from '../models/register-request.model';
import { User } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_BASE_URL = 'http://localhost:8000/api';
  private readonly TOKEN_KEY = 'auth_token';
  private readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private readonly USER_KEY = 'current_user';

  private currentUserSubject = new BehaviorSubject<User | null>(this.getUserFromStorage());
  public currentUser$ = this.currentUserSubject.asObservable();

  private isAuthenticatedSubject = new BehaviorSubject<boolean>(this.hasValidToken());
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.checkTokenExpiration();
  }

  register(registerData: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.API_BASE_URL}/auth/register`, registerData)
      .pipe(
        tap(response => {
          this.handleAuthResponse(response);
        }),
        catchError(this.handleError)
      );
  }

  login(loginData: LoginRequest): Observable<AuthResponse> {
    // Convert to form data for OAuth2 compatibility
    const formData = new FormData();
    formData.append('username', loginData.email);
    formData.append('password', loginData.password);

    return this.http.post<AuthResponse>(`${this.API_BASE_URL}/auth/login`, formData)
      .pipe(
        tap(response => {
          this.handleAuthResponse(response);
        }),
        catchError(this.handleError)
      );
  }

  logout(): Observable<any> {
    return this.http.post(`${this.API_BASE_URL}/auth/logout`, {})
      .pipe(
        tap(() => {
          this.clearAuthData();
        }),
        catchError(() => {
          // Even if logout fails on server, clear local data
          this.clearAuthData();
          return throwError(() => new Error('Logout failed'));
        })
      );
  }

  getCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.API_BASE_URL}/auth/me`)
      .pipe(
        tap(user => {
          this.setUser(user);
        }),
        catchError(this.handleError)
      );
  }

  refreshToken(): Observable<AuthResponse> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      return throwError(() => new Error('No refresh token available'));
    }

    return this.http.post<AuthResponse>(`${this.API_BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken
    }).pipe(
      tap(response => {
        this.handleAuthResponse(response);
      }),
      catchError(error => {
        this.clearAuthData();
        return this.handleError(error);
      })
    );
  }

  isAuthenticated(): boolean {
    return this.hasValidToken();
  }

  getCurrentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  private handleAuthResponse(response: AuthResponse): void {
    if (response.access_token) {
      localStorage.setItem(this.TOKEN_KEY, response.access_token);

      if (response.refresh_token) {
        localStorage.setItem(this.REFRESH_TOKEN_KEY, response.refresh_token);
      }

      this.isAuthenticatedSubject.next(true);

      // Get user profile after successful auth
      this.getCurrentUser().subscribe({
        next: (user) => {
          console.log('User profile loaded:', user);
        },
        error: (error) => {
          console.error('Failed to load user profile:', error);
        }
      });
    }
  }

  private clearAuthData(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
    this.router.navigate(['/auth/login']).catch(error => {
      console.error('Navigation to login failed:', error);
    });
  }

  private setUser(user: User): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    this.currentUserSubject.next(user);
  }

  private getUserFromStorage(): User | null {
    const userJson = localStorage.getItem(this.USER_KEY);
    if (userJson) {
      try {
        return JSON.parse(userJson);
      } catch {
        localStorage.removeItem(this.USER_KEY);
      }
    }
    return null;
  }

  private hasValidToken(): boolean {
    const token = this.getAccessToken();
    if (!token) {
      return false;
    }

    try {
      // Basic JWT expiration check
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch {
      return false;
    }
  }

  private checkTokenExpiration(): void {
    setInterval(() => {
      if (!this.hasValidToken() && this.isAuthenticatedSubject.value) {
        console.log('Token expired, attempting refresh...');
        this.refreshToken().subscribe({
          error: () => {
            console.log('Token refresh failed, logging out...');
            this.clearAuthData();
          }
        });
      }
    }, 60000); // Check every minute
  }

  private handleError = (error: HttpErrorResponse): Observable<never> => {
    let errorMessage: string = 'An unknown error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = error.error.message;
    } else {
      // Server-side error
      if (error.error?.detail) {
        errorMessage = error.error.detail;
      } else if (error.message) {
        errorMessage = error.message;
      } else {
        errorMessage = `Server error: ${error.status}`;
      }
    }

    console.error('Auth Service Error:', error);
    return throwError(() => new Error(errorMessage));
  };
}
