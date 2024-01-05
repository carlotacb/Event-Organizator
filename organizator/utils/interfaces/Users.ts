// eslint-disable-next-line no-shadow
export enum UserRoles {
  ORGANIZER_ADMIN = "Organizer admin",
  ORGANIZER = "Organizer",
  PARTICIPANT = "Participant",
}

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

export interface LoginFormFields {
  username: string;
  password: string;
}

export interface LoginResponse {
  readonly token: string;
  readonly error: string | null;
}

export interface UserInformation {
  readonly id: string;
  readonly username: string;
  readonly email: string;
  readonly firstName: string;
  readonly lastName: string;
  readonly bio: string;
  readonly profileImage: string;
  readonly role: string;
}

export interface UserInformationResponse {
  readonly error: string | null;
  readonly userInformation: UserInformation | null;
}

export interface UpdateFormFields {
  firstName: string;
  lastName: string;
  bio: string;
}

export interface GetRoleResponse {
  readonly error: string | null;
  readonly role: string | null;
}

export interface UserRoleInformation {
  readonly id: string;
  readonly username: string;
  readonly role: string;
}

export interface AllUserResponse {
  readonly error: string | null;
  readonly users: UserRoleInformation[] | null;
}

export interface UpdateRoleResponse {
  readonly error: string | null;
  readonly user: UserRoleInformation | null;
}
