import React, { useEffect, useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  View,
} from "react-native";
import { router, useLocalSearchParams } from "expo-router";
// @ts-ignore
import styled from "styled-components/native";
import { ConfirmDialog } from "react-native-simple-dialogs";
import Toast from "react-native-toast-message";
import { EventInformation } from "../../../utils/interfaces/Events";
import {
  deleteEvent,
  getEventById,
  updateEvent,
} from "../../../utils/api/axiosEvents";
import {
  formatDate,
  getColorForApplicationStatus,
} from "../../../utils/util-functions";
import LoadingPage from "../../../components/Pages/LodingPage";
import EmptyPage from "../../../components/Pages/EmptyPage";
import Button from "../../../components/componentsStyled/Buttons/ButtonWithIcon";
import { getToken } from "../../../utils/sessionCalls";
import { getUserRole } from "../../../utils/api/axiosUsers";
import { UserRoles } from "../../../utils/interfaces/Users";
import {
  getApplicationStatus,
  createNewApplication,
} from "../../../utils/api/axiosApplications";
import InformativeChip from "../../../components/componentsStyled/Chips/InformativeChip";
import { ButtonsRowContainerLeft } from "../../../components/componentsStyled/Shared/ContainerStyles";
import { systemColors } from "../../../components/componentsStyled/tokens";
import EventForm from "../../../components/componentsStyled/Forms/EventForm";
import EventDetails from "../../../components/componentsStyled/EventDetails";

const Container = styled(SafeAreaView)`
  background-color: white;
  flex: 1;
`;

const ImageHeader = styled.Image`
  height: 200px;
`;

const TextLine = styled.View`
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
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
    headerImage: "",
    onlyForStudents: false,
    openForParticipants: true,
  });
  const [isOrganizer, setIsOrganizer] = React.useState(false);
  const [isOrganizerAdmin, setIsOrganizerAdmin] = React.useState(false);
  const [isParticipant, setIsParticipant] = React.useState(false);
  const [applied, setApplied] = React.useState(false);
  const [applicationStatus, setApplicationStatus] = React.useState("");
  const [trigger, setTrigger] = React.useState(false);

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
        headerImage: response.eventInformation?.headerImage || "",
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
  }, [trigger]);

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

  const updateTheEvent = () => {
    setLoading(true);
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
        setTrigger(!trigger);
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
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        enabled={isEditable}
      >
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
                        <ButtonsRowContainerLeft>
                          <Button
                            title="Close"
                            onPress={() => {
                              setIsEditable(false);
                            }}
                            color={systemColors.destroy}
                            iconName="close"
                          />
                        </ButtonsRowContainerLeft>
                        <EventForm
                          inputs={inputs}
                          setInputs={setInputs}
                          createTheEvent={updateTheEvent}
                          isUpdate
                        />
                      </View>
                    ) : (
                      <View style={{ padding: 30 }}>
                        <ButtonsRowContainerLeft>
                          {isParticipant ? (
                            applied ? (
                              <AppliedContainer>
                                <TextLine>
                                  <ApplicationStatus>
                                    Your application is:
                                  </ApplicationStatus>
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
                          ) : isEditable ? null : (
                            <>
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
                            </>
                          )}
                        </ButtonsRowContainerLeft>
                        <EventDetails event={events} />
                      </View>
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
      </KeyboardAvoidingView>
      <Toast />
    </Container>
  );
}
