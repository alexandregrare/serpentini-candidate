import data from './data/input.json' assert {type: 'json'};
import fs from 'fs';

let totalSells = [];
let userIds = [];
let userObjectives = [];
let result = {
  "commissions" : []
};

// Fill informations lists with users' data
data.users.map((elem) => {
  totalSells.push(0)
  userIds.push(elem['id'])
  userObjectives.push(elem['objective'])
});

// Fill users' total sells amount
data.deals.map((elem) => {
  let idArrayIndex = userIds.indexOf(elem['user']); // Get index of the user's id in the array of ids
  totalSells[idArrayIndex] += elem['amount'];
});

userIds.map((id, index) => {
  let userCommission = 0
  const objectiveHalf = userObjectives[index] / 2;

  // First part of the commission (between 0% and 50% of the objective)
  userCommission += Math.min(objectiveHalf, totalSells[index]) * 5 / 100;
  totalSells[index] -= Math.min(objectiveHalf, totalSells[index]);
  if (totalSells[index] > objectiveHalf) {
    // Add second part of the commission (between 50% and 100% of the objective)
    userCommission += Math.min(objectiveHalf, totalSells[index]) * 10 / 100;
    totalSells[index] -= Math.min(objectiveHalf, totalSells[index]);
  }
  // Add 15% of the remaining sales amount
  userCommission += totalSells[index] * 15 / 100;
  result.commissions.push(
    {
      "user_id": id,
      "commission": userCommission
    });
});

// Write result in output file
fs.writeFile('./output.json', JSON.stringify(result), err => {
  if (err) {
    console.error(err);
  }
});
