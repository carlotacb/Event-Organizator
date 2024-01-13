import React, { useEffect, useState } from "react";
import { SafeAreaView, ScrollView, Text, View } from "react-native";
import { Link, router, useLocalSearchParams } from "expo-router";
// @ts-ignore
import styled from "styled-components/native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import { ConfirmDialog } from "react-native-simple-dialogs";
import Toast from "react-native-toast-message";
import { EventInformation } from "../../../utils/interfaces/Events";
import {
  deleteEvent,
  getEventById,
  updateEvent,
} from "../../../utils/api/axiosEvents";
import {
  checkDateRange,
  checkDateWithTime,
  dateToPlainString,
  formatDate,
  getColorForApplicationStatus,
  parseDate,
} from "../../../utils/util-functions";
import LoadingPage from "../../../components/Pages/LodingPage";
import EmptyPage from "../../../components/Pages/EmptyPage";
import Input from "../../../components/componentsStyled/Forms/Input";
import Button from "../../../components/componentsStyled/Buttons/ButtonWithIcon";
import { getToken } from "../../../utils/sessionCalls";
import { getUserRole } from "../../../utils/api/axiosUsers";
import { UserRoles } from "../../../utils/interfaces/Users";
import {
  getApplicationStatus,
  createNewApplication,
} from "../../../utils/api/axiosApplications";
import FilterButton from "../../../components/componentsStyled/Buttons/FilterButtons";
import InformativeChip from "../../../components/componentsStyled/Chips/InformativeChip";
import { Title } from "../../../components/componentsStyled/Shared/TextStyles";
import {
  BottomScreenContainer,
  ButtonsRowContainer,
} from "../../../components/componentsStyled/Shared/ContainerStyles";
import { systemColors } from "../../../components/componentsStyled/tokens";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const ImageHeader = styled.Image`
  height: 200px;
`;

const InformationContainer = styled.View`
  padding: 30px 20px;
`;

const Description = styled.Text`
  color: #7f7f7f;
  margin-top: 20px;
  font-size: 18px;
`;

const BasicInfoContainer = styled.View`
  margin-top: 30px;
  background-color: rgba(164, 164, 164, 0.38);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const RestrictionContainer = styled.View`
  margin-top: 30px;
  background-color: rgba(138, 159, 243, 0.2);
  border: 2px solid rgb(138, 159, 243);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const TextLine = styled.View`
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
`;

const StyledLink = styled(Link)`
  color: blue;
  font-weight: bold;
`;

const ApplicationStatus = styled.Text`
  font-size: 18px;
  color: dimgray;
  font-weight: bold;
`;

const AppliedContainer = styled.View`
  display: flex;
`;

export default function EventPage() {
  const { id } = useLocalSearchParams();
  const [loading, setLoading] = React.useState(true);
  const [events, setEvents] = React.useState<EventInformation | null>(null);
  const [showAlert, setShowAlert] = React.useState(false);
  const [isEditable, setIsEditable] = React.useState(false);
  const [inputs, setInputs] = useState({
    name: "",
    url: "",
    description: "",
    startDate: "",
    endDate: "",
    location: "",
    maxParticipants: "",
    attritionRate: "",
    minAge: "",
    onlyForStudents: false,
    openForParticipants: true,
  });
  const [errors, setErrors] = React.useState({
    name: undefined,
    url: undefined,
    description: undefined,
    startDate: undefined,
    endDate: undefined,
    location: undefined,
    maxParticipants: undefined,
    attritionRate: undefined,
    minAge: undefined,
  });
  const [isOrganizer, setIsOrganizer] = React.useState(false);
  const [isOrganizerAdmin, setIsOrganizerAdmin] = React.useState(false);
  const [isParticipant, setIsParticipant] = React.useState(false);
  const [applied, setApplied] = React.useState(false);
  const [applicationStatus, setApplicationStatus] = React.useState("");

  useEffect(() => {
    // @ts-ignore
    const fetchData = async () => getEventById(id);
    const fetchRoleFunction = async () => {
      const t = await getToken();
      return getUserRole(t);
    };

    const fetchApplicationStatus = async () => {
      const tkn = await getToken();
      // @ts-ignore
      return getApplicationStatus(tkn || "", id);
    };

    fetchData().then((response) => {
      setLoading(false);
      setEvents(response.eventInformation || null);
      setInputs({
        name: response.eventInformation?.name || "",
        url: response.eventInformation?.url || "",
        description: response.eventInformation?.description || "",
        startDate: formatDate(response.eventInformation?.startDate || ""),
        endDate: formatDate(response.eventInformation?.endDate || ""),
        location: response.eventInformation?.location || "",
        maxParticipants: response.eventInformation?.maxParticipants || "",
        attritionRate: response.eventInformation?.attritionRate || "",
        minAge: response.eventInformation?.minAge || "",
        onlyForStudents: response.eventInformation?.onlyForStudents || false,
        openForParticipants:
          response.eventInformation?.openForParticipants || true,
      });
    });

    fetchRoleFunction().then((response) => {
      setIsOrganizer(response.role === UserRoles.ORGANIZER);
      setIsOrganizerAdmin(response.role === UserRoles.ORGANIZER_ADMIN);
      setIsParticipant(response.role === UserRoles.PARTICIPANT);
    });

    fetchApplicationStatus().then((response) => {
      if (response.notApplied) {
        setApplied(false);
      } else {
        setApplied(true);
        setApplicationStatus(response.status || "");
      }
    });
  }, []);

  const deleteThisEvent = () => {
    const fetchData = async () => {
      const token = await getToken();
      // @ts-ignore
      return deleteEvent(token || "", id);
    };

    fetchData().then(() => {
      setShowAlert(false);
      router.back();
    });
  };

  const handleOnChange = (text: string, input: string) => {
    setInputs((prevState) => ({ ...prevState, [input]: text }));
  };
  const handleError = (text: string | undefined, input: string) => {
    setErrors((prevState) => ({ ...prevState, [input]: text }));
  };

  const validate = () => {
    let isValid = true;

    if (!inputs.name) {
      handleError("Please enter a name for the event", "name");
      isValid = false;
    } else {
      handleError(undefined, "name");
    }

    if (!inputs.url) {
      handleError("Please enter a url for the event", "url");
      isValid = false;
    } else {
      handleError(undefined, "url");
    }

    if (!inputs.description) {
      handleError("Please enter a description for the event", "description");
      isValid = false;
    } else {
      handleError(undefined, "description");
    }

    if (!inputs.startDate) {
      handleError("Please enter a starting date for the event", "startDate");
      isValid = false;
    } else {
      const dateChecker = checkDateWithTime(inputs.startDate);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "startDate");
        isValid = false;
      } else {
        const today = new Date();
        const validRange = checkDateRange(
          dateToPlainString(today),
          inputs.startDate,
        );
        if (!validRange.valid) {
          handleError(validRange.error, "startDate");
          isValid = false;
        } else {
          handleError(undefined, "startDate");
        }
      }
    }

    if (!inputs.endDate) {
      handleError("Please enter a ending date for the event", "endDate");
      isValid = false;
    } else {
      const dateChecker = checkDateWithTime(inputs.endDate);
      if (!dateChecker.valid) {
        handleError(dateChecker.error, "endDate");
        isValid = false;
      } else {
        const validRange = checkDateRange(inputs.startDate, inputs.endDate);
        if (!validRange.valid) {
          handleError(validRange.error, "endDate");
          isValid = false;
        } else {
          handleError(undefined, "endDate");
        }
      }
    }

    if (!inputs.location) {
      handleError("Please enter a location for the event", "location");
      isValid = false;
    } else {
      handleError(undefined, "location");
    }

    if (!inputs.maxParticipants) {
      handleError(
        "Please enter a max participants for the event",
        "maxParticipants",
      );
      isValid = false;
    } else {
      const isNum = /^\d+$/.test(inputs.maxParticipants);
      if (!isNum) {
        handleError("Please enter a valid number", "maxParticipants");
        isValid = false;
      } else {
        handleError(undefined, "maxParticipants");
      }
    }

    if (!inputs.attritionRate) {
      handleError(
        "Please enter the expected attrition rate for the event",
        "attritionRate",
      );
      isValid = false;
    } else {
      const isNum = /^\d+$/.test(inputs.attritionRate);
      if (!isNum) {
        handleError("Please enter a valid number", "attritionRate");
        isValid = false;
      } else {
        handleError(undefined, "attritionRate");
      }
    }

    if (!inputs.minAge) {
      handleError(
        "Please enter the minimum age to participate in the event",
        "minAge",
      );
      isValid = false;
    } else {
      const isNum = /^\d+$/.test(inputs.minAge);
      if (!isNum) {
        handleError("Please enter a valid number", "minAge");
        isValid = false;
      } else {
        handleError(undefined, "minAge");
      }
    }

    if (isValid) {
      setLoading(true);
      // @ts-ignore

      const fetchData = async () => {
        const token = await getToken();
        // @ts-ignore
        return updateEvent(token || "", inputs, id);
      };

      fetchData().then((response) => {
        if (response.error) {
          Toast.show({
            type: "error",
            text1: "Error",
            text2: response.error,
            visibilityTime: 8000,
          });
        } else {
          setEvents(response.eventInformation || null);
          Toast.show({
            type: "success",
            text1: "Success",
            text2: "Event updated successfully",
            visibilityTime: 8000,
          });
          setIsEditable(false);
          setLoading(false);
        }
      });
    }
  };

  const applyToEvent = () => {
    const fetchData = async () => {
      const token = await getToken();
      // @ts-ignore
      return createNewApplication(id, token || "");
    };

    fetchData().then((response) => {
      if (response.error) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: response.error,
          visibilityTime: 2000,
        });
      } else {
        Toast.show({
          type: "success",
          text1: "Success",
          text2: "You have applied to this event",
          visibilityTime: 2000,
        });
      }
    });
  };

  return (
    <Container>
      <ScrollView>
        {loading ? (
          <LoadingPage />
        ) : (
          <View>
            {events?.deleted ? (
              <EmptyPage
                title={`The event ${events?.name} has been removed`}
                subtitle="To know more about it, contact the organizers"
                image={require("../../../assets/deleted.webp")}
              />
            ) : (
              <View>
                <ImageHeader source={{ uri: events?.headerImage }} />
                <View>
                  {isEditable ? (
                    <View style={{ padding: 30 }}>
                      <Input
                        label="Event name"
                        iconName="tag"
                        required
                        value={inputs.name}
                        onChangeText={(text) => handleOnChange(text, "name")}
                        error={errors.name}
                      />
                      <Input
                        label="Webpage url"
                        iconName="link"
                        required
                        value={inputs.url}
                        onChangeText={(text) => handleOnChange(text, "url")}
                        error={errors.url}
                      />
                      <Input
                        label="Start date"
                        iconName="hourglass-start"
                        required
                        value={inputs.startDate}
                        onChangeText={(text) =>
                          handleOnChange(text, "startDate")
                        }
                        error={errors.startDate}
                      />
                      <Input
                        label="End date"
                        iconName="hourglass-end"
                        required
                        value={inputs.endDate}
                        onChangeText={(text) => handleOnChange(text, "endDate")}
                        error={errors.endDate}
                      />
                      <Input
                        label="Location"
                        iconName="map-marker"
                        required
                        value={inputs.location}
                        onChangeText={(text) =>
                          handleOnChange(text, "location")
                        }
                        error={errors.location}
                      />
                      <View
                        style={{
                          display: "flex",
                          flexDirection: "row",
                          justifyContent: "space-between",
                        }}
                      >
                        <Input
                          label="Max participants"
                          iconName="users"
                          required
                          value={inputs.maxParticipants}
                          onChangeText={(text) =>
                            handleOnChange(text, "maxParticipants")
                          }
                          error={errors.maxParticipants}
                          width="45%"
                          inputMode="numeric"
                          keyboardType="numeric"
                        />
                        <Input
                          label="Attrition rate (%)"
                          iconName="percent"
                          required
                          value={inputs.attritionRate}
                          onChangeText={(text) =>
                            handleOnChange(text, "attritionRate")
                          }
                          error={errors.attritionRate}
                          width="45%"
                          inputMode="decimal"
                          keyboardType="numeric"
                        />
                      </View>
                      <View
                        style={{
                          display: "flex",
                          flexDirection: "row",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}
                      >
                        <Input
                          label="Minimum age"
                          iconName="calendar-minus-o"
                          required
                          value={inputs.minAge}
                          onChangeText={(text) =>
                            handleOnChange(text, "minAge")
                          }
                          error={errors.minAge}
                          width="45%"
                          inputMode="numeric"
                          keyboardType="numeric"
                        />
                        <FilterButton
                          onPress={() => {
                            setInputs((prevState) => ({
                              ...prevState,
                              onlyForStudents: !prevState.onlyForStudents,
                            }));
                          }}
                          color="dimgray"
                          iconName="graduation-cap"
                          title="Only for students"
                          width="45%"
                          active={inputs.onlyForStudents}
                        />
                      </View>
                      <Input
                        label="Description"
                        iconName="pencil"
                        required
                        multiline
                        numberOfLines={4}
                        value={inputs.description}
                        onChangeText={(text) =>
                          handleOnChange(text, "description")
                        }
                        error={errors.description}
                      />
                      <FilterButton
                        onPress={() => {
                          setInputs((prevState) => ({
                            ...prevState,
                            openForParticipants: !prevState.openForParticipants,
                          }));
                        }}
                        color="dimgray"
                        iconName="edit"
                        title="Open for participants to apply"
                        active={inputs.openForParticipants}
                      />
                    </View>
                  ) : (
                    <InformationContainer>
                      <Title>{events?.name}</Title>
                      <Description>{events?.description}</Description>
                      <BasicInfoContainer>
                        <TextLine>
                          <FontAwesome name="hourglass-start" />
                          <Text>
                            The event is starting on{" "}
                            {parseDate(events?.startDate || "")}
                          </Text>
                        </TextLine>
                        <TextLine>
                          <FontAwesome name="hourglass-end" />
                          <Text>
                            The event is ending on{" "}
                            {parseDate(events?.endDate || "")}
                          </Text>
                        </TextLine>
                        <TextLine>
                          <FontAwesome name="map-marker" />
                          <Text>
                            The event will take place in {events?.location}
                          </Text>
                        </TextLine>
                        <TextLine>
                          <FontAwesome name="link" />
                          <Text>
                            Find all the information in{" "}
                            <StyledLink href={events?.url || ""}>
                              here
                            </StyledLink>
                          </Text>
                        </TextLine>
                      </BasicInfoContainer>
                      <RestrictionContainer>
                        <TextLine>
                          <Text>
                            The minimum age to participate is: {events?.minAge}
                          </Text>
                        </TextLine>
                        <TextLine>
                          <Text>
                            The event is open for{" "}
                            {events?.onlyForStudents
                              ? "only students"
                              : "everyone"}
                          </Text>
                        </TextLine>
                      </RestrictionContainer>
                    </InformationContainer>
                  )}
                </View>
              </View>
            )}
          </View>
        )}
        <ConfirmDialog
          title={`Delete ${events?.name}`}
          message="Are you sure about that? This action will not be undone"
          onTouchOutside={() => setShowAlert(false)}
          visible={showAlert}
          negativeButton={{
            title: "Cancel",
            onPress: () => {
              setShowAlert(false);
            },
            titleStyle: {
              color: "red",
              fontSize: 20,
            },
            style: {
              backgroundColor: "transparent",
              paddingHorizontal: 10,
            },
          }}
          positiveButton={{
            title: "Delete!",
            onPress: () => {
              deleteThisEvent();
            },
            titleStyle: {
              color: "blue",
              fontSize: 20,
            },
            style: {
              backgroundColor: "transparent",
              paddingHorizontal: 10,
            },
          }}
          contentInsetAdjustmentBehavior="automatic"
          onRequestClose={() => setShowAlert(false)}
        />
      </ScrollView>

      {!loading && !events?.deleted && (
        <BottomScreenContainer>
          {isParticipant ? (
            applied ? (
              <AppliedContainer>
                <TextLine>
                  <ApplicationStatus>Your application is:</ApplicationStatus>
                  <InformativeChip
                    name={applicationStatus}
                    backgroundColor={getColorForApplicationStatus(
                      applicationStatus,
                    )}
                  />
                </TextLine>
              </AppliedContainer>
            ) : (
              <Button
                title="Apply now"
                onPress={() => {
                  applyToEvent();
                }}
                color={systemColors.action}
              />
            )
          ) : isEditable ? (
            <ButtonsRowContainer>
              <Button
                title="Save"
                onPress={validate}
                color={systemColors.accept}
                iconName="save"
              />
              <Button
                title="Cancel"
                onPress={() => {
                  setIsEditable(false);
                }}
                color={systemColors.destroy}
                iconName="close"
              />
            </ButtonsRowContainer>
          ) : (
            <ButtonsRowContainer>
              {(isOrganizer || isOrganizerAdmin) && (
                <Button
                  title="Edit"
                  onPress={() => {
                    setIsEditable(true);
                  }}
                  color={systemColors.edit}
                  iconName="pencil"
                />
              )}
              {isOrganizerAdmin && (
                <Button
                  title="Delete"
                  onPress={() => {
                    setShowAlert(true);
                  }}
                  color={systemColors.destroy}
                  iconName="trash"
                />
              )}
            </ButtonsRowContainer>
          )}
        </BottomScreenContainer>
      )}
      <Toast />
    </Container>
  );
}
