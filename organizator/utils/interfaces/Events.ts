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
  maxParticipants: string;
  attritionRate: string;
  minAge: string;
  onlyForStudents: boolean;
  openForParticipants: boolean;
}

export interface EventCardProps {
  id: string;
  name: string;
  startDate: string;
  endDate: string;
  location: string;
  headerImage: string;
}

export interface CreateEventProps {
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  location: string;
  headerImage: string;
  url: string;
  openForParticipants: boolean;
  maxParticipants: string;
  attritionRate: string;
  minAge: string;
  onlyForStudents: boolean;
}

export interface UpdateEventProps {
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  location: string;
  url: string;
  openForParticipants: boolean;
  maxParticipants: string;
  attritionRate: string;
  minAge: string;
  onlyForStudents: boolean;
}

export interface getAllEventResponse {
  readonly error: string | null;
  readonly eventInformation: EventAllInformation[] | null;
}

export interface getEventResponse {
  readonly error: string | null;
  readonly eventInformation: EventInformation | null;
}

export interface updateEventResponse {
  readonly error: string | null;
  readonly eventInformation: EventInformation | null;
}

export interface deleteEventResponse {
  readonly error: string | null;
}

export interface createEventResponse {
  readonly error: string | null;
}

export interface EventsSimpleInformationWithParticipants {
  name: string;
  actual_participants_count: number;
  max_participants: number;
  expected_attrition_rate: number;
}

export interface getUpcomingEventsWithApplicationsInfoResponse {
  readonly events: EventsSimpleInformationWithParticipants[] | null;
  readonly error: string | null;
}
