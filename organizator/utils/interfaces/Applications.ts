import { EventAllInformation } from "./Events";

export interface CreateNewApplicationResponse {
  readonly error: string | null;
}

export interface GetMyApplicationsResponse {
  readonly error: string | null;
  readonly applications: ApplicationInformationWithoutUser[] | null;
}

export interface ApplicationInformationWithoutUser {
  readonly id: string;
  readonly event: EventAllInformation;
  readonly status: string;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface ParticipantsInformation {
  id: string;
  user: {
    id: string;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    bio: string;
    profile_image: string;
    role: string;
    date_of_birth: string;
    study: boolean;
    work: boolean;
    university: string;
    degree: string;
    current_job_role: string;
    tshirt: string;
    gender: string;
    alimentary_restrictions: string;
    github: string;
    linkedin: string;
    devpost: string;
    webpage: string;
    expected_graduation: string;
  };
  status: string;
  event_name: string;
  event_start_date: string;
  event_end_date: string;
  created_at: string;
  updated_at: string;
}

export interface GetParticipantsResponse {
  readonly error: string | null;
  readonly participants: ParticipantsInformation[] | null;
}

export interface updateApplicationStatusResponse {
  readonly error: string | null;
}

export interface applicationStatusResponse {
  readonly error: string | null;
  readonly status: string | null;
  readonly notApplied: boolean;
}

export interface cancelApplicationResponse {
  readonly error: string | null;
}

export interface confirmApplicationResponse {
  readonly error: string | null;
}
