import axios from "axios";
import {
  EventAllInformation,
  getAllEventResponse,
  getEventResponse,
} from "../interfaces/Events";

const eventsAPI = "http://0.0.0.0:8000/organizator-api/events";

export async function getAllEvents(): Promise<getAllEventResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${eventsAPI}/`,
    });
    return { error: null, eventInformation: [...response.data] };
  } catch (error: any) {
    return {
      error: error.response.data,
      eventInformation: null,
    };
  }
}

export async function getEventById(eventId: string): Promise<getEventResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${eventsAPI}/${eventId}`,
    });
    return {
      error: null,
      eventInformation: {
        deleted: !!response.data.deleted,
        description: response.data.description,
        endDate: response.data.end_date,
        headerImage: response.data.header_image,
        id: response.data.id,
        location: response.data.location,
        name: response.data.name,
        startDate: response.data.start_date,
        url: response.data.url,
      },
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      eventInformation: null,
    };
  }
}
