import axios from "axios";
import {
  applicationStatusResponse,
  cancelApplicationResponse,
  CreateNewApplicationResponse,
  GetMyApplicationsResponse,
  GetParticipantsResponse,
  updateApplicationStatusResponse,
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

export async function updateApplicationStatus(
  token: string,
  applicationId: string,
  status: string,
): Promise<updateApplicationStatusResponse> {
  try {
    await axios({
      method: "post",
      url: `${applicationsAPI}/update/${applicationId}`,
      data: { status },
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

export async function getApplicationStatus(
  token: string,
  eventId: string,
): Promise<applicationStatusResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${applicationsAPI}/status/${eventId}`,
      headers: {
        Authorization: `${token}`,
      },
    });

    if (response.status === 206) {
      return {
        error: null,
        status: null,
        notApplied: true,
      };
    }

    return {
      error: null,
      status: response.data.status,
      notApplied: false,
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      status: null,
      notApplied: false,
    };
  }
}

export async function cancelApplication(
  token: string,
  applicationId: string,
): Promise<cancelApplicationResponse> {
  try {
    await axios({
      method: "post",
      url: `${applicationsAPI}/cancel/${applicationId}`,
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
