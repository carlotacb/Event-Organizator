import axios from "axios";
import { CreateNewApplicationResponse } from "../interfaces/Applications";

const applicationsAPI = "http://0.0.0.0:8000/organizator-api/applications";

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
