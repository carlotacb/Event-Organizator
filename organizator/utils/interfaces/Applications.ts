import { EventAllInformation, EventInformation } from "./Events";

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
  readonly created_at: string;
  readonly updated_at: string;
}
