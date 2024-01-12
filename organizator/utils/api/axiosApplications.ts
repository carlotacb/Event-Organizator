import axios from "axios";
import {
  CreateNewApplicationResponse,
  GetMyApplicationsResponse,
  GetParticipantsResponse,
} from "../interfaces/Applications";
import { applicationsAPI } from "./constants";

export async function createNewApplication(
  eventId: string,
  token: string,
): Promise<CreateNewApplicationResponse> {
  try {
    await axios({
      method: "post",
      url: `${applicationsAPI}/new`,
      data: { event_id: eventId },
      headers: {
        Authorization: `${token}`,
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

export async function getMyApplications(
  token: string,
): Promise<GetMyApplicationsResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${applicationsAPI}/myevents`,
      headers: {
        Authorization: `${token}`,
      },
    });
    return {
      error: null,
      applications: response.data,
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      applications: null,
    };
  }
}

export async function getParticipants(
  token: string,
  eventId: string,
): Promise<GetParticipantsResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${applicationsAPI}/participants/${eventId}`,
      headers: {
        Authorization: `${token}`,
      },
    });
    return {
      error: null,
      participants: [...response.data],
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      participants: null,
    };
  }
}
