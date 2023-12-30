import { Image, Text, View } from "react-native";
import React from "react";
// @ts-ignore
import styled from "styled-components/native";

interface EmptyPageProps {
  title: string;
  subtitle: string;
  image: any;
}

const NoEventsContainer = styled(View)`
  padding: 100px 50px;
  align-items: center;
`;

const Title = styled(Text)`
  font-size: 30px;
  font-weight: bold;
  color: black;
  text-align: center;
`;

const SubTitle = styled(Text)`
  font-size: 18px;
  color: gray;
  margin: 5px 0 20px 0;
  text-align: center;
`;

export default function EmptyPage(props: EmptyPageProps) {
  const { title, subtitle, image } = props;

  return (
    <NoEventsContainer>
      <Title>{title}</Title>
      <SubTitle>{subtitle}</SubTitle>
      <Image
        source={image}
        style={{ width: 280, height: 280, alignSelf: "center" }}
      />
    </NoEventsContainer>
  );
}
