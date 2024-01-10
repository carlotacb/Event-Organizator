import axios from "axios";
import {
  AllUserResponse,
  GetRoleResponse,
  LoginFormFields,
  LoginResponse,
  RegisterFields,
  RegisterFormFields,
  RegisterResponse,
  UpdateFormFields,
  UpdateRoleResponse,
  UserInformationResponse,
} from "../interfaces/Users";
import { usersAPI } from "./constants";

const baseImage =
  "https://media.istockphoto.com/id/1087531642/vector/male-face-silhouette-or-icon-man-avatar-profile-unknown-or-anonymous-person-vector.jpg?s=612x612&w=0&k=20&c=FEppaMMfyIYV2HJ6Ty8tLmPL1GX6Tz9u9Y8SCRrkD-o%3D";

export async function registerUser(
  data: RegisterFormFields,
  isWorking: boolean,
  isStudying: boolean,
): Promise<RegisterResponse> {
  try {
    await axios({
      method: "post",
      url: `${usersAPI}/new`,
      data: JSON.stringify(
        serializerToRegisterFields(data, isWorking, isStudying),
      ),
    });
    return { error: null };
  } catch (error: any) {
    return {
      error: error.response.data,
    };
  }
}

function serializerToRegisterFields(
  data: RegisterFormFields,
  isWorking: boolean,
  isStudying: boolean,
): RegisterFields {
  return {
    email: data.email,
    password: data.password,
    first_name: data.firstName,
    last_name: data.lastName,
    username: data.username,
    bio: data.bio,
    profile_image: baseImage,
    date_of_birth: data.dateOfBirth,
    current_job_role: isWorking ? data.currentJobRole : null,
    university: isStudying ? data.university : null,
    degree: isStudying ? data.degree : null,
    expected_graduation: isStudying ? data.graduationYear : null,
    study: isStudying,
    work: isWorking,
  };
}

export async function loginUser(data: LoginFormFields): Promise<LoginResponse> {
  try {
    const response = await axios({
      method: "post",
      url: `${usersAPI}/login`,
      data: JSON.stringify(data),
    });
    return { error: null, token: response.data.token };
  } catch (error: any) {
    return {
      error: error.response.data,
      token: "",
    };
  }
}

export async function logout(token: string | null) {
  try {
    await axios({
      method: "post",
      url: `${usersAPI}/logout`,
      headers: {
        Authorization: `${token}`,
      },
    });
  } catch (error: any) {
    console.log(error);
  }
}

export async function getMyInformation(
  token: string | null,
): Promise<UserInformationResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${usersAPI}/me`,
      headers: {
        Authorization: `${token}`,
      },
    });
    return {
      error: null,
      userInformation: {
        id: response.data.id,
        bio: response.data.bio,
        email: response.data.email,
        firstName: response.data.first_name,
        lastName: response.data.last_name,
        profileImage: response.data.profile_image,
        username: response.data.username,
        role: response.data.role,
        tShirtSize: response.data.tshirt,
        alimentaryRestrictions: response.data.alimentary_restrictions,
        dateOfBirth: response.data.date_of_birth,
        gender: response.data.gender,
        github: response.data.github,
        linkedin: response.data.linkedin,
        devpost: response.data.devpost,
        webpage: response.data.webpage,
        study: response.data.study,
        university: response.data.university,
        degree: response.data.degree,
        expectedGraduation: response.data.expected_graduation,
        work: response.data.work,
        currentJobRole: response.data.current_job_role,
      },
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      userInformation: null,
    };
  }
}

function parseCorrectGender(gender: string): string {
  let parsed = gender;
  if (gender === "Male") parsed = "MALE";
  if (gender === "Female") parsed = "FEMALE";
  if (gender === "No-binary") parsed = "NO_BINARY";
  if (gender === "Prefer not to say") parsed = "PREFER_NOT_TO_SAY";

  return parsed;
}

export async function updateMyInformation(
  data: UpdateFormFields,
  token: string,
  isStudying: boolean,
  isWorking: boolean,
): Promise<UserInformationResponse> {
  try {
    const response = await axios({
      method: "post",
      url: `${usersAPI}/update/me`,
      data: JSON.stringify({
        first_name: data.firstName,
        last_name: data.lastName,
        bio: data.bio,
        tshirt: data.tShirtSize,
        alimentary_restrictions: data.alimentaryRestrictions,
        date_of_birth: data.dateOfBirth,
        gender: parseCorrectGender(data.gender),
        github: data.github,
        linkedin: data.linkedin,
        devpost: data.devpost,
        webpage: data.webpage,
        study: isStudying,
        work: isWorking,
        current_job_role: isWorking ? data.currentJobRole : null,
        university: isStudying ? data.university : null,
        degree: isStudying ? data.degree : null,
        expected_graduation: isStudying ? data.expectedGraduation : null,
      }),
      headers: {
        Authorization: token,
      },
    });
    return {
      error: null,
      userInformation: {
        id: response.data.id,
        bio: response.data.bio,
        email: response.data.email,
        firstName: response.data.first_name,
        lastName: response.data.last_name,
        profileImage: response.data.profile_image,
        username: response.data.username,
        role: response.data.role,
        tShirtSize: response.data.tshirt,
        alimentaryRestrictions: response.data.alimentary_restrictions,
        dateOfBirth: response.data.date_of_birth,
        gender: response.data.gender,
        github: response.data.github,
        linkedin: response.data.linkedin,
        devpost: response.data.devpost,
        webpage: response.data.webpage,
        study: response.data.study,
        university: response.data.university,
        degree: response.data.degree,
        expectedGraduation: response.data.expected_graduation,
        work: response.data.work,
        currentJobRole: response.data.current_job_role,
      },
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      userInformation: null,
    };
  }
}

export async function getUserRole(
  token: string | null,
): Promise<GetRoleResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${usersAPI}/me/role`,
      headers: {
        Authorization: `${token}`,
      },
    });
    return {
      error: null,
      role: response.data.role,
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      role: null,
    };
  }
}

export async function getAllUsersRoles(): Promise<AllUserResponse> {
  try {
    const response = await axios({
      method: "get",
      url: `${usersAPI}/`,
    });
    return {
      error: null,
      users: [...response.data],
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      users: null,
    };
  }
}

export async function updateRoleForUser(
  id: string,
  token: string,
  role: string,
): Promise<UpdateRoleResponse> {
  try {
    const response = await axios({
      method: "post",
      url: `${usersAPI}/update/role/${id}`,
      data: { role },
      headers: {
        Authorization: `${token}`,
      },
    });
    return {
      error: null,
      user: response.data,
    };
  } catch (error: any) {
    return {
      error: error.response.data,
      user: null,
    };
  }
}
