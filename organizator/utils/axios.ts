import axios from "axios";
import { EventAllInformation } from "./Interfaces";

interface getAllEventResponse {
  readonly error: string | null;
  readonly eventInformation: EventAllInformation[] | null;
}

const eventsAPI = "http://0.0.0.0:8000/organizator-api/events/";

export async function getAllEvents(): Promise<getAllEventResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${eventsAPI}`,
    });
    return { error: null, eventInformation: { ...response.data } };
  } catch (error) {
    console.log(error);
    return {
      error: "unexpected error",
      eventInformation: null,
    };
  }
}
