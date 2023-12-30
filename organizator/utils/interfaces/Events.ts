// This interface is in snake case because it's the information coming from the API
export interface EventAllInformation {
  deleted: boolean;
  description: string;
  end_date: string;
  header_image: string;
  id: string;
  location: string;
  name: string;
  start_date: string;
  url: string;
}

export interface EventInformation {
  deleted: boolean;
  description: string;
  endDate: string;
  headerImage: string;
  id: string;
  location: string;
  name: string;
  startDate: string;
  url: string;
}

export interface EventCardProps {
  id: string;
  name: string;
  startDate: string;
  endDate: string;
  location: string;
  headerImage: string;
}

export interface getAllEventResponse {
  readonly error: string | null;
  readonly eventInformation: EventAllInformation[] | null;
}

export interface getEventResponse {
  readonly error: string | null;
  readonly eventInformation: EventInformation | null;
}

export interface deleteEventResponse {
  readonly error: string | null;
}
