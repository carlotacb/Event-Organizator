import axios from "axios";
import {
  CreateNewApplicationResponse,
  GetMyApplicationsResponse,
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
