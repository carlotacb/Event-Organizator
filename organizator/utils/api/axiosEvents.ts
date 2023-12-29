import axios from "axios";
import { EventAllInformation } from "../interfaces/Events";

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
      headers: {
        "X-CSRFTOKEN": "OWMpm5pWe5INbqlV9ZXOWwlIENDIYldi",
      },
    });
    return { error: null, eventInformation: [...response.data] };
  } catch (error: any) {
    return {
      error: error.response.data,
      eventInformation: null,
    };
  }
}
