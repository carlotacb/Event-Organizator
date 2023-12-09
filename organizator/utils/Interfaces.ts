// This interface is in snake case because it's the information coming from the API
export interface EventAllInformation {
  id: string;
  name: string;
  url: string;
  description: string;
  start_date: string;
  end_date: string;
  location: string;
  header_image: string;
}

export interface EventCardProps {
  id: string;
  name: string;
  startDate: string;
  endDate: string;
  location: string;
  headerImage: string;
}
