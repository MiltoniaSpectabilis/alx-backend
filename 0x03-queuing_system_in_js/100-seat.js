import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();
const getAsync = promisify(client.get).bind(client);

let reservationEnabled = true;

const reserveSeat = (number) => {
  client.set('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10);
};

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  const currentSeats = await getCurrentAvailableSeats();
  if (currentSeats === 0) {
    reservationEnabled = false;
  }

  if (currentSeats >= 0) {
    reserveSeat(currentSeats - 1);
  } else {
    queue.create('reserve_seat').failed(new Error('Not enough seats available'));
  }
});

app.listen(1245, () => {
  console.log('Server is running on port 1245');
  reserveSeat(50);
});
