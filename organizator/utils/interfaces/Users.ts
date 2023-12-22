export interface RegisterFields {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  username: string;
  bio: string;
  profile_image: string;
}

export interface RegisterFormFields {
  username: string;
  email: string;
  password: string;
  passwordConfirm: string;
  firstName: string;
  lastName: string;
  bio: string;
}

export interface RegisterResponse {
  readonly error: string | null;
}
