import axios from "axios";
import {
  CreateEventProps,
  createEventResponse,
  deleteEventResponse,
  getAllEventResponse,
  getEventResponse,
  UpdateEventProps,
  updateEventResponse,
} from "../interfaces/Events";

const eventsAPI = "http://0.0.0.0:8000/organizator-api/events";

export async function getAllUpcomingEvents(): Promise<getAllEventResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${eventsAPI}/upcoming`,
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

export async function deleteEvent(
  eventId: string,
): Promise<deleteEventResponse> {
  try {
    await axios({
      method: "post",
      url: `${eventsAPI}/delete/${eventId}`,
    });
    return {
      error: null,
    };
  } catch (error: any) {
    return {
      error: error.response.data,
    };
  }
}

export async function createEvent(
  eventInformation: CreateEventProps,
): Promise<createEventResponse> {
  try {
    await axios({
      method: "post",
      url: `${eventsAPI}/new`,
      data: {
        name: eventInformation.name,
        description: eventInformation.description,
        start_date: eventInformation.startDate,
        end_date: eventInformation.endDate,
        location: eventInformation.location,
        header_image: eventInformation.headerImage,
        url: eventInformation.url,
      },
    });
    return {
      error: null,
    };
  } catch (error: any) {
    return {
      error: error.response.data,
    };
  }
}

export async function updateEvent(
  eventInformation: UpdateEventProps,
  eventId: string,
): Promise<updateEventResponse> {
  try {
    const response = await axios({
      method: "post",
      url: `${eventsAPI}/update/${eventId}`,
      data: {
        name: eventInformation.name,
        description: eventInformation.description,
        start_date: eventInformation.startDate,
        end_date: eventInformation.endDate,
        location: eventInformation.location,
        url: eventInformation.url,
      },
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
