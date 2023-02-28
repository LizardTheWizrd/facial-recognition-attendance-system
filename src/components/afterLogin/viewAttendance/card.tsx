import {
  Box,
  Text,
} from '@chakra-ui/react';
import axios from 'axios';
import React, { useState, useEffect, useContext } from 'react'
import { WeekContext } from '../../context';


const Hero: React.FC = () => {
  const {weekNumber, setWeekNumber} = useContext(WeekContext);
  const {subjectCodeNumber, setSubjectCodeNumber} = useContext(WeekContext);
  const {sessionNumberCon, setSessionNumberConNumber} = useContext(WeekContext);

  const URL = 'http://127.0.0.1:5000/api/test/attendance/csci369/1?week=';
  
  const [data, setData] = useState<Array<{ 
    student_id: number; 
    student_name: string; 
    week: string;
    date: string;
    attedance_percentage: string;
    status: string;
    unexcused_absences: string; 
  }>>([]);

  useEffect(() => {
    
    const fetchData = async () => {
      const result = await axios.get(URL + weekNumber);
      setData(result.data);
      console.log(subjectCodeNumber + " " + sessionNumberCon);
    };

    fetchData();
  }, [weekNumber]);

  return (
    <>
      {data.map((item) => (  
        <Box paddingLeft="2%" h="13%" display="flex">  
                
          <Box w='10%' display="flex" alignItems="center">
            <Text>{item.student_id}</Text>
          </Box>
          <Box w='13%' display="flex" alignItems="center">
            <Text>{item.student_name}</Text>
          </Box>
          <Box w='7%' display="flex" alignItems="center">
            <Text>{item.week}</Text>
          </Box>
          <Box w='8%' display="flex" alignItems="center">
            <Text>{item.date}</Text>
          </Box>
          <Box w='15%' display="flex" alignItems="center">
            <Text>{item.attedance_percentage + "%"}</Text>
          </Box>
          <Box w='15%' display="flex" alignItems="center">
            <Text>{item.status}</Text>
          </Box>
          <Box w='15%' display="flex" alignItems="center">
            <Text>{item.unexcused_absences}</Text>
          </Box>
        </Box>
      ))}
    </>
  );
};

export default Hero;
