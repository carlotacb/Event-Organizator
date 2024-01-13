// @ts-ignore
import styled from "styled-components/native";

export const CardContainer = styled.View<{ isPast: boolean }>`
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  margin: 10px;
  width: 300px;
  opacity: ${(props: { isPast: boolean }) => (props.isPast ? 0.5 : 1)};
`;

export const CardImage = styled.Image`
  height: 200px;
  border-radius: 20px;
`;

export const CardTextContainer = styled.View`
  padding: 25px 25px 20px;
`;

export const CardTitle = styled.Text`
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
`;

export const CardText = styled.Text`
  font-size: 16px;
`;

export const TextLine = styled.View`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
`;
