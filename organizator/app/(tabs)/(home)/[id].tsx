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
import parseDate from "../../../utils/util-functions";
import LoadingPage from "../../../components/LodingPage";
import EmptyPage from "../../../components/EmptyPage";
import Input from "../../../components/Input";
import Button from "../../../components/ButtonWithIcon";

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

const Title = styled.Text`
  text-align: center;
  font-weight: bold;
  font-size: 30px;
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

const ButtonsContainer = styled.View`
  display: flex;
  flex-direction: row;
  margin-top: 30px;
  justify-content: center;
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
  });
  const [errors, setErrors] = React.useState({
    name: undefined,
    url: undefined,
    description: undefined,
    startDate: undefined,
    endDate: undefined,
    location: undefined,
  });

  useEffect(() => {
    // @ts-ignore
    const fetchData = async () => getEventById(id);

    fetchData().then((response) => {
      setLoading(false);
      setEvents(response.eventInformation || null);
      setInputs({
        name: response.eventInformation?.name || "",
        url: response.eventInformation?.url || "",
        description: response.eventInformation?.description || "",
        startDate: response.eventInformation?.startDate || "",
        endDate: response.eventInformation?.endDate || "",
        location: response.eventInformation?.location || "",
      });
    });
  }, []);

  const deleteThisEvent = () => {
    // @ts-ignore
    deleteEvent(id)
      .then(() => {
        setShowAlert(false);
        router.replace("/");
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleOnChange = (text: string, input: string) => {
    setInputs((prevState) => ({ ...prevState, [input]: text }));
  };
  const handleError = (text: string | undefined, input: string) => {
    setErrors((prevState) => ({ ...prevState, [input]: text }));
  };

  const validate = () => {
    let isValid = false;

    if (!inputs.name) {
      handleError("Please enter a name for the event", "name");
    } else {
      handleError(undefined, "name");
    }

    if (!inputs.url) {
      handleError("Please enter a url for the event", "url");
    } else {
      handleError(undefined, "url");
    }

    if (!inputs.description) {
      handleError("Please enter a description for the event", "description");
    } else {
      handleError(undefined, "description");
    }

    if (!inputs.startDate) {
      handleError("Please enter a starting date for the event", "startDate");
    } else {
      handleError(undefined, "startDate");
    }

    if (!inputs.endDate) {
      handleError("Please enter a ending date for the event", "endDate");
    } else {
      handleError(undefined, "endDate");
    }

    if (!inputs.location) {
      handleError("Please enter a location for the event", "location");
    } else {
      handleError(undefined, "location");
    }

    if (
      errors.name === undefined &&
      errors.url === undefined &&
      errors.description === undefined &&
      errors.startDate === undefined &&
      errors.endDate === undefined &&
      errors.location === undefined
    ) {
      isValid = true;
    }

    if (isValid) {
      setLoading(true);
      // @ts-ignore
      updateEvent(inputs, id).then((response) => {
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

                      <ButtonsContainer>
                        <Button
                          title="Save"
                          onPress={validate}
                          color="#58a659"
                          iconName="save"
                        />
                        <Button
                          title="Cancel"
                          onPress={() => {
                            setIsEditable(false);
                          }}
                          color="#f07267"
                          iconName="close"
                        />
                      </ButtonsContainer>
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
                      <ButtonsContainer>
                        <Button
                          title="Edit"
                          onPress={() => {
                            setIsEditable(true);
                          }}
                          color="#58a659"
                          iconName="pencil"
                        />
                        <Button
                          title="Delete"
                          onPress={() => {
                            setShowAlert(true);
                          }}
                          color="#f07267"
                          iconName="trash"
                        />
                      </ButtonsContainer>
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
      <Toast />
    </Container>
  );
}
