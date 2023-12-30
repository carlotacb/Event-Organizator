import React, { useEffect } from "react";
import { SafeAreaView, ScrollView, Text, View } from "react-native";
import { Link, router, useLocalSearchParams } from "expo-router";
// @ts-ignore
import styled from "styled-components/native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import { ConfirmDialog } from "react-native-simple-dialogs";
import { EventInformation } from "../../../utils/interfaces/Events";
import { deleteEvent, getEventById } from "../../../utils/api/axiosEvents";
import parseDate from "../../../utils/util-functions";
import ButtonWithIcon from "../../../components/ButtonWithIcon";
import LoadingPage from "../../../components/LodingPage";
import EmptyPage from "../../../components/EmptyPage";

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

  useEffect(() => {
    // @ts-ignore
    const fetchData = async () => getEventById(id);

    fetchData().then((response) => {
      setLoading(false);
      setEvents(response.eventInformation || null);
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
              <>
                <ImageHeader source={{ uri: events?.headerImage }} />
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
                        <StyledLink href={events?.url || ""}>here</StyledLink>
                      </Text>
                    </TextLine>
                  </BasicInfoContainer>
                  <ButtonsContainer>
                    <ButtonWithIcon
                      title="Edit"
                      onPress={() => {}}
                      color="#58a659"
                      iconName="pencil"
                    />
                    <ButtonWithIcon
                      title="Delete"
                      onPress={() => {
                        setShowAlert(true);
                      }}
                      color="#f07267"
                      iconName="trash"
                    />
                  </ButtonsContainer>
                </InformationContainer>
              </>
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
    </Container>
  );
}
