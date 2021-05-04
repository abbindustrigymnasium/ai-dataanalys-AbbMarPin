/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
<template>
  <div class="minesweeper">
    <div class="minesweeper-status">
      <div class="minesweeper-bombcount">
        {{ bombCount }}
      </div>
      <a href="#" @click.prevent="initGrid"> &#9786; </a>
      <minesweeper-timer
        class="minesweeper-timer"
        :finished="finished"
      ></minesweeper-timer>
      <v-switch
        class="my-n1"
        label="Cheat"
        @change="toggleCheat()"
        v-model="cheat"
      ></v-switch>
    </div>
    <!-- <v-btn color="success" class="ma-2" @click="select()"
      >select next targets</v-btn
    > -->
    <v-row align="center">
      <v-col class="d-flex" cols="12" sm="6">
        <v-btn color="success" class="ma-2" @click="EzGame()">EZGame</v-btn>
      </v-col>
      <v-col>
        <v-select
          :items="[0, 1, 10, 100]"
          v-model="delay"
          label="Delay"
        ></v-select>
      </v-col>
    </v-row>

    <v-btn
      color="success"
      class="ma-2"
      @click="cheatOnce(grid.find((cell) => cell.selected))"
      >cheatOnce</v-btn
    >
    <!-- <v-btn color="success" class="ma-2" @click="updateAllCells()"
      >update all</v-btn
    > -->

    <div class="minesweeper-grid" :style="getGridStyle()">
      <minesweeper-cell
        v-for="(cell, i) in grid"
        :key="i"
        :cell="cell"
        @click.native="clickCell(cell, i, true)"
        @click.right.native="addFlag(cell)"
        @dblclick.native.prevent="doubleClick(cell, i)"
        @contextmenu.native.prevent
      >
      </minesweeper-cell>
    </div>
  </div>
</template>

<script lang="ts">
import MinesweeperCell from "./MinesweeperCell.vue";
import MinesweeperTimer from "./MinesweeperTimer.vue";
import Vue from "vue";

interface cell {
  hasBomb: Boolean;
  bombCount: Number;
  isOpen: Boolean;
  openNear: number;
  hasFlag: Boolean;
  flaggedNear: number;
  neighborhood: number[] | null;
  hiddenNeighborhood: number[] | null;
  cheat: Boolean;
  selected: number;
  Index: number;
}

export default Vue.extend({
  name: "minesweeper-game",
  components: {
    MinesweeperCell,
    MinesweeperTimer,
  },
  props: {
    cols: {
      type: Number,
      default: 10,
    },
    rows: {
      type: Number,
      default: 30,
    },
    bombs: {
      type: Number,
      default: 55,
    },
  },
  data() {
    return {
      bombCount: 0,
      finished: false,
      won: false,
      grid: [] as cell[],
      cheat: true,
      selectNext: false,
      selected: [] as number[][],
      targetI: -1,
      flagTarget: false,
      delay: 0,
    };
  },
  mounted() {
    this.initGrid();
    this.toggleCheat();
  },
  computed: {
    allBombs() {
      this.grid.filter((cell) => {
        cell;
      });
    },
  },
  methods: {
    wait(ms: number) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    async EzGame() {
      let orig: cell[] = [];
      while (!this.won) {
        // find good game
        console.log("Starting...");
        this.initGrid();
        orig = [];
        let moves = 0;
        this.finished = false;
        // debugger

        while (!this.finished) {
          // find good moves
          if (this.checkLost()) break;
          this.cheatOnce();
          if (this.selected.length && !orig.length) {
            this.grid.forEach((cell: cell) => {
              orig.push({
                hasBomb: cell.hasBomb,
                bombCount: cell.bombCount,
                isOpen: cell.isOpen,
                openNear: cell.openNear,
                hasFlag: cell.hasFlag,
                flaggedNear: cell.flaggedNear,
                neighborhood: cell.neighborhood,
                cheat: cell.cheat,
                selected: cell.selected,
                hiddenNeighborhood: cell.hiddenNeighborhood,
                Index: cell.Index,
              });
            });
          }
          moves++;
          if (this.delay) await this.wait(this.delay);
        }
        console.log("Got Finished game in", moves);
      }

      console.log("Finished");
      console.log("Setting board");
      // console.log(orig, this.grid, orig == this.grid)
      this.grid = orig;

      // ------------------------------------------------
      // Reset
      this.grid.forEach((cell: cell) => (cell.selected = 0));
      this.finished = false;
      this.won = false;
    },
    updateAllCells() {
      // console.log(this.selected, this.targetI);

      this.grid.forEach((cell: cell, i) => {
        let n = 0;
        this.getNeighborhood(cell).forEach((i) => {
          let neighbourCell = this.grid[i];
          if (!neighbourCell.isOpen) {
            n++;
          }
        });
        cell.openNear = n;

        let n2 = 0;
        this.getNeighborhood(cell).forEach((i) => {
          let neighbourCell = this.grid[i];
          if (neighbourCell.hasFlag) {
            n2++;
          }
        });
        cell.flaggedNear = n2;

        let n3 = [] as number[];
        this.getNeighborhood(cell).forEach((i) => {
          let neighbourCell = this.grid[i];
          if (!neighbourCell.isOpen) {
            n3.push(i);
          }
        });
        cell.hiddenNeighborhood = n3;
      });
    },
    select() {
      this.grid.forEach((cell: cell, i) => {
        if (cell.isOpen) {
          if (cell.hiddenNeighborhood?.length == cell.bombCount) {
            this.addAllHiddenNear(i, 1);
          }
        }
      });

      this.grid.forEach((cell: cell, i) => {
        if (cell.isOpen) {
          if (cell.bombCount == cell.flaggedNear) {
            this.addAllHiddenNear(i, 0);
          }
        }
      });

      if (this.selected.length == 0) {
        this.pickRandom();
      }

      // console.log(this.selected);

      // let good = false;
      // let i: number;

      // while (!good) {
      //   // i = Math.floor(Math.random() * this.grid.length);
      //   const goodPlaces = this.grid.filter((cell) => cell.bombCount != 0);
      //   i = Math.floor(Math.random() * goodPlaces.length);
      //   let cell = goodPlaces[i];
      //   i = cell.Index;
      //   console.log("checking:", cell, i, goodPlaces);
      //   this.checkNeighborhood(cell, false);
      //   if (!cell.neighborhood) continue;

      //   cell.neighborhood.forEach((ii) => {
      //     let neighbor = this.grid[ii];
      //     if (!neighbor.isOpen) {
      //       good = true;
      //       this.grid.forEach((cell: cell) => {
      //         cell.selected = false;
      //       });
      //       this.grid[i].selected = true;
      //       console.log("Selecting:", this.grid[i], i);
      //       return;
      //     }
      //   });
      // }
    },
    pickRandom() {
      let closed = this.grid.filter((cell) => !cell.isOpen);
      let i = Math.floor(Math.random() * closed.length);
      this.clickCell(closed[i], closed[i].Index, false);
      console.warn("Picking random cell:", closed[i]);
    },
    addAllHiddenNear(i: number, oneIfBomb: number): void {
      if (!this.grid[i].isOpen) {
        return;
      }

      this.getNeighborhood(this.grid[i]).forEach((ii) => {
        let cell = this.grid[ii];
        // console.log("going through:", i, "neighbour", ii, "Open:", cell.isOpen, "Selected", cell.selected)
        if (!cell.isOpen && !cell.selected) {
          this.selected.push([ii, oneIfBomb]);
          cell.selected = 1 + oneIfBomb;
        }
      });
    },
    toggleCheat() {
      console.log(this.grid);
      this.grid.forEach((cell: cell) => {
        cell.cheat = this.cheat;
      });
    },
    cheatOnce() {
      if (this.finished) {
        console.warn("Alredy Finished!");
        return -1;
      }
      // console.log("First", this.selected, this.targetI);
      // -1 = no target

      if (this.targetI != -1) {
        let cell: cell = this.grid[this.targetI];
        // console.log("Goin for", cell, this.flagTarget);

        if (this.flagTarget) {
          if (!cell.hasFlag) {
            // console.log("addFlag", cell);
            this.addFlag(cell);
          }
        } else {
          if (cell.hasFlag) {
            console.error("Flag bad", cell);
          } else {
            // console.log("clickCell", cell);
            this.clickCell(cell, cell.Index, false);
          }
        }
      }

      this.updateAllCells();

      this.selected = this.selected.filter(
        (i: number[]) => !this.grid[i[0]].isOpen && !this.grid[i[0]].hasFlag
      );

      if (this.selected.length) {
        this.targetI = this.selected[0][0];
        this.flagTarget = Boolean(this.selected[0][1]);
      } else {
        this.select();
      }
      // console.log("Last", this.selected, this.targetI);

      // this.setNeighborhood(cell, cell.Index);
      // console.log("cheat cell:", cell);
      // if (!cell.neighborhood) return;
      // let totClosed = 0;
      // cell.neighborhood.forEach((i) => {
      //   let neighbor = this.grid[i];
      //   console.log("neighbor:", neighbor, neighbor.isOpen)
      //   if (!neighbor.isOpen) {
      //     totClosed++;
      //   }
      // });
      // console.log("closed", totClosed, cell.bombCount);

      // if (totClosed == cell.bombCount) {

      //   cell.neighborhood.forEach((i) => {
      //     let neighbor = this.grid[i];
      //     if (!neighbor.isOpen) {

      //       this.addFlag(neighbor);
      //     }
      //   });
      // }
    },
    getGridStyle() {
      const { cols } = this;
      return `grid-template-columns: repeat(${cols}, 1fr);`;
    },
    initGrid() {
      this.targetI = -1;
      this.flagTarget = false;
      this.selected = [];

      let { bombs } = this;
      const { cols, rows } = this;
      const size = rows * cols;
      const grid: cell[] = [];
      if (bombs > size) {
        console.log("more bombs than space on the grid!");
        return;
      }
      for (let i = 0; i < size; i += 1) {
        grid.push({
          hasBomb: false,
          bombCount: 0,
          isOpen: false,
          openNear: 0,
          hasFlag: false,
          flaggedNear: 0,
          neighborhood: null,
          cheat: false,
          selected: 0,
          hiddenNeighborhood: null,
          Index: i,
        });
      }
      while (bombs > 0) {
        const num = Math.floor(Math.random() * size);
        if (grid[num].hasBomb === false) {
          bombs -= 1;
          grid[num].hasBomb = true;
        }
      }
      this.grid = grid;
      this.finished = true;
      this.$nextTick(() => {
        this.finished = false;
      });
      this.won = false;
      this.bombCount = this.bombs;
      this.toggleCheat();
    },
    haveWeWon() {
      if (this.finished) {
        return;
      }
      if (this.bombCount !== 0) {
        return;
      }
      const remainingGrid = this.grid.find((g) => !g.isOpen && !g.hasFlag);
      if (!remainingGrid) {
        this.finished = true;
        this.won = true;
      }
    },
    addFlag(cell: cell) {
      if (this.finished) {
        return;
      }
      if (cell.isOpen) {
        return;
      }
      cell.hasFlag = !cell.hasFlag;
      const { grid } = this;
      const flagCount = grid.reduce((accumulator, currentValue) => {
        if (currentValue.hasFlag) {
          return accumulator + 1;
        }
        return accumulator;
      }, 0);
      this.bombCount = this.bombs - flagCount;
      this.haveWeWon();
    },
    doubleClick(cell: cell, i: number) {
      if (this.finished) {
        return;
      }
      if (cell.isOpen === false) {
        return;
      }
      this.setNeighborhood(cell, i);
      if (!cell.bombCount) {
        return;
      }

      const { grid } = this;
      let flagCount = 0;
      cell.neighborhood?.forEach((j: number) => {
        if (grid[j].hasFlag) {
          flagCount += 1;
        }
      });
      if (flagCount === cell.bombCount) {
        this.checkNeighborhood(cell, true);
      }
    },
    clickCell(cell: cell, i: number, isUser: Boolean) {
      if (isUser) {
        console.log(cell, i);
      }
      if (this.selectNext) {
        this.grid.forEach((cell: cell) => {
          cell.selected = 0;
        });
        cell.selected = 1;
        this.selectNext = false;
        return;
      }
      if (this.finished) {
        return;
      }
      if (cell.hasFlag) {
        return;
      }
      if (cell.isOpen) {
        if (isUser) {
          this.doubleClick(cell, i);
          console.log(cell, i);
        }
        return;
      }
      if (cell.hasBomb) {
        // todo bomb!
        const { grid } = this;
        grid.forEach((checkCell: cell) => {
          if (checkCell.hasBomb) {
            checkCell.isOpen = true;
          }
        });
        this.finished = true;
        return;
      }

      this.setNeighborhood(cell, i);
      cell.isOpen = true;
      this.checkNeighborhood(cell, undefined);
      this.haveWeWon();
    },
    checkNeighborhood(cell: cell, force: boolean | undefined) {
      if (cell.bombCount !== 0 && force !== true) {
        return;
      }

      const { grid } = this;
      if (cell.neighborhood) {
        cell.neighborhood.forEach((i) => {
          this.clickCell(grid[i], i, false);
        });
      }
    },
    getNeighborhood(cell: cell) {
      let neighborhood = [];
      for (let x = -1; x < 2; x += 1) {
        for (let y = -1; y < 2; y += 1) {
          const cellIndex = this.getIndex(cell.Index, x, y);
          if (cellIndex !== false) {
            neighborhood.push(cellIndex);
          }
        }
      }
      return neighborhood;
    },
    setNeighborhood(cell: cell, i: number) {
      if (cell.neighborhood !== null) {
        return;
      }
      const { grid } = this;
      const neighborhood = [];
      let bombCount = 0;
      for (let x = -1; x < 2; x += 1) {
        for (let y = -1; y < 2; y += 1) {
          const cellIndex = this.getIndex(i, x, y);
          if (cellIndex !== false) {
            neighborhood.push(cellIndex);
            if (grid[cellIndex].hasBomb) {
              bombCount += 1;
            }
          }
        }
      }
      cell.bombCount = bombCount;
      cell.neighborhood = neighborhood;
    },
    getIndex(i: number, x: number, y: number) {
      const { cols, rows } = this;
      if (x === 0 && y === 0) {
        return false;
      }
      if ((i % cols) + x < 0 || (i % cols) + x >= cols) {
        return false;
      }
      if (Math.floor(i / cols) + y < 0 || Math.floor(i / cols) + y >= rows) {
        return false;
      }
      return i + (y * cols + x);
    },
    checkLost() {
      return Boolean(
        this.grid.some((cell: cell) => cell.isOpen && cell.hasBomb)
      );
    },
  },
  watch: {
    rows() {
      this.initGrid();
    },
    cols() {
      this.initGrid();
    },
    bombs() {
      this.initGrid();
    },
  },
});
</script>

<style lang="scss">
.minesweeper {
  &-status {
    display: flex;
    justify-content: space-between;
    padding: 1rem;

    > * {
      flex: 1;
      text-align: center;
    }
  }

  &-grid {
    user-select: none;
    position: relative;
    overflow: auto;
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    grid-auto-rows: 1fr;

    &:before {
      content: "";
      width: 0;
      padding-bottom: 100%;
      grid-row: 1 / 1;
      grid-column: 1 / 1;
    }

    > *:first-child {
      grid-row: 1 / 1;
      grid-column: 1 / 1;
    }
  }
}
</style>
