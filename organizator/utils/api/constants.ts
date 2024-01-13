const baseURLdevelopment = "http://0.0.0.0:8000/organizator-api";
const baseURLproduction =
  "https://event-organizator-api-c6wz5mj4uq-ew.a.run.app/organizator-api";

const usingURL = baseURLproduction;

export const usersAPI = `${usingURL}/users`;
export const eventsAPI = `${usingURL}/events`;
export const applicationsAPI = `${usingURL}/applications`;
