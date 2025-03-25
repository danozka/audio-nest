import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly _registerUrl = '/api/auth/register';
  private readonly _tokenUrl = '/api/auth/token';

  constructor(private _http: HttpClient) { }

  register(userData: { username: string; password: string }): Observable<any> {
    return this._http.post(this._registerUrl, userData);
  }
}
