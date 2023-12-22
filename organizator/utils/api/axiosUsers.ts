import axios from "axios";
import {
  RegisterFields,
  RegisterFormFields,
  RegisterResponse,
} from "../interfaces/Users";

const usersAPI = "http://0.0.0.0:8000/organizator-api/users";

export default async function registerUser(
  data: RegisterFormFields,
): Promise<RegisterResponse> {
  try {
    await axios({
      method: "post",
      url: `${usersAPI}/new`,
      data: JSON.stringify(serializerToRegisterFields(data)),
    });
    return { error: null };
  } catch (error: any) {
    return {
      error: error.response.data,
    };
  }
}

function serializerToRegisterFields(data: RegisterFormFields): RegisterFields {
  return {
    email: data.email,
    password: data.password,
    first_name: data.firstName,
    last_name: data.lastName,
    username: data.username,
    bio: data.bio,
    profile_image:
      "https://media.istockphoto.com/id/1087531642/vector/male-face-silhouette-or-icon-man-avatar-profile-unknown-or-anonymous-person-vector.jpg?s=612x612&w=0&k=20&c=FEppaMMfyIYV2HJ6Ty8tLmPL1GX6Tz9u9Y8SCRrkD-o%3D",
  };
}
