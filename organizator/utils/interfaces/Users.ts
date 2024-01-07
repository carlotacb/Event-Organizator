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
  date_of_birth: string;
  current_job_role: string | null;
  university: string | null;
  degree: string | null;
  expected_graduation: string | null;
  study: boolean;
  work: boolean;
}

export interface RegisterFormFields {
  username: string;
  email: string;
  password: string;
  passwordConfirm: string;
  firstName: string;
  lastName: string;
  bio: string;
  dateOfBirth: string;
  currentJobRole: string;
  university: string;
  degree: string;
  graduationYear: string;
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
  readonly tShirtSize: string;
  readonly alimentaryRestrictions: string;
  readonly dateOfBirth: string;
  readonly gender: string;
  readonly github: string;
  readonly linkedin: string;
  readonly devpost: string;
  readonly webpage: string;
  readonly study: boolean;
  readonly university: string;
  readonly degree: string;
  readonly expectedGraduation: string;
  readonly work: boolean;
  readonly currentJobRole: string;
}

export interface UserInformationResponse {
  readonly error: string | null;
  readonly userInformation: UserInformation | null;
}

export interface UpdateFormFields {
  firstName: string;
  lastName: string;
  bio: string;
  tShirtSize: string;
  alimentaryRestrictions: string;
  dateOfBirth: string;
  gender: string;
  github: string;
  linkedin: string;
  devpost: string;
  webpage: string;
  university: string;
  degree: string;
  expectedGraduation: string;
  currentJobRole: string;
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
