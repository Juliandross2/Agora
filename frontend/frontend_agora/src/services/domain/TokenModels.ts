import type { User } from "./UsuarioModels";

export interface LoginRequest {
  email_usuario: string;
  contrasenia: string;
}

export interface LoginResponse {
  message: string;
  user: User;
  refresh: string;
  access: string;
}