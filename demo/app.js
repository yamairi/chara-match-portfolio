let currentProduct = DEMO_DATA.products[0];
let currentCharacter = currentProduct.characters[0];


const categorySelect =
  document.getElementById("categorySelect");

const productSelect =
  document.getElementById("productSelect");



function init() {

  setupCategories();

  updateProductList();

  render();

}


function setupCategories() {

  const categories =
    [...new Set(
      DEMO_DATA.products.map(
        p => p.category
      )
    )];


  categorySelect.innerHTML =
    categories
      .map(
        category =>
          `<option value="${category}">
             ${category}
           </option>`
      )
      .join("");

}


function updateProductList() {

  const category =
    categorySelect.value;


  const products =
    DEMO_DATA.products.filter(
      p => p.category === category
    );


  productSelect.innerHTML =
    products
      .map(
        p =>
          `<option value="${p.id}">
             ${p.name}
           </option>`
      )
      .join("");


  currentProduct = products[0];

  currentCharacter =
    currentProduct.characters[0];

}



categorySelect.addEventListener(
  "change",
  () => {

    updateProductList();

    render();

  }
);



productSelect.addEventListener(
  "change",
  () => {

    currentProduct =
      DEMO_DATA.products.find(
        p => p.id === productSelect.value
      );


    currentCharacter =
      currentProduct.characters[0];


    render();

  }
);



function render() {

  renderProduct();

  renderRanking();

  renderMatrix();

  renderCandidates();

  renderCharacter();

}



function renderProduct() {

  document.getElementById("price")
    .textContent =
      currentProduct.price;


  document.getElementById("target")
    .textContent =
      currentProduct.target;


  document.getElementById("description")
    .textContent =
      currentProduct.description;


  document.getElementById("keywords")
    .innerHTML =
      currentProduct.keywords
        .map(
          keyword =>
            `<span class="tag">
              ${keyword}
            </span>`
        )
        .join("");

}



function renderRanking() {

  const container =
    document.getElementById("typeRanking");


  container.innerHTML =
    currentProduct.types
      .map(
        (type, index) => {

          return `

          <div class="rank-row">

            <div class="rank-number">
              ${index + 1}
            </div>

            <div class="rank-content">

              <strong>
                ${type.name}
              </strong>

              <div class="score-bar">

                <div
                  class="score-fill"
                  style="width:${type.score}%">
                </div>

              </div>

            </div>

            <div class="rank-score">
              ${type.score}
            </div>

          </div>

          `;

        }
      )
      .join("");

}



function renderMatrix() {

  const matrix =
    document.getElementById("matrix");


  matrix
    .querySelectorAll(".matrix-point")
    .forEach(
      el => el.remove()
    );


  currentProduct.types.forEach(
    (type, index) => {

      const point =
        document.createElement("div");


      point.className =
        index === 0
          ? "matrix-point main-point"
          : "matrix-point";


      point.style.left =
        `${type.compatibility}%`;


      point.style.bottom =
        `${type.expansion}%`;


      point.title =
        `${type.name}
Compatibility ${type.compatibility}
Expansion ${type.expansion}`;


      matrix.appendChild(point);

    }
  );


  const best =
    currentProduct.types[0];


  document.getElementById(
    "matrixExplanation"
  ).textContent =

    `${best.name}は、
     Compatibility ${best.compatibility}、
     Expansion ${best.expansion}。
     現在顧客との親和性と、
     新市場への拡張余地を
     同時に比較しています。`;

}



function renderCandidates() {

  const container =
    document.getElementById(
      "candidateList"
    );


  container.innerHTML =
    currentProduct.characters
      .map(
        (character, index) => {

          return `

          <button
            class="candidate ${
              character.name ===
              currentCharacter.name
                ? "active"
                : ""
            }"

            onclick="
              selectCharacter(${index})
            "
          >

            <div>

              <strong>
                ${character.name}
              </strong>

              <span>
                ${character.type}
              </span>

            </div>

            <div class="candidate-score">
              ${character.score}
            </div>

            <div class="arrow">
              ›
            </div>

          </button>

          `;

        }
      )
      .join("");

}



function selectCharacter(index) {

  currentCharacter =
    currentProduct.characters[index];


  renderCandidates();

  renderCharacter();


  document
    .querySelector(".detail-panel")
    .scrollIntoView({
      behavior: "smooth"
    });

}



function renderCharacter() {

  const c =
    currentCharacter;


  document.getElementById(
    "characterName"
  ).textContent =
    c.name;


  document.getElementById(
    "characterType"
  ).textContent =
    c.type;


  document.getElementById(
    "totalScore"
  ).textContent =
    c.score;


  document.getElementById(
    "compatibility"
  ).textContent =
    c.compatibility;


  document.getElementById(
    "expansion"
  ).textContent =
    c.expansion;


  document.getElementById(
    "unexpected"
  ).textContent =
    c.unexpected;


  document.getElementById(
    "reliability"
  ).textContent =
    c.reliability;


  document.getElementById(
    "reason"
  ).textContent =
    c.reason;


  document.getElementById(
    "candidateTags"
  ).innerHTML =
    c.tags
      .map(
        tag =>
          `<span class="tag">
            ${tag}
          </span>`
      )
      .join("");


  renderSegments();

}



function renderSegments() {

  const names = [
    "Segment A",
    "Segment B",
    "Segment C",
    "Segment D",
    "Segment E"
  ];


  const container =
    document.getElementById(
      "segmentChart"
    );


  container.innerHTML =
    names
      .map(
        (name, index) => {

          const current =
            currentProduct
              .customerSegments[index];


          const character =
            currentCharacter
              .supporterSegments[index];


          const diff =
            character - current;


          return `

          <div class="segment-row">

            <div class="segment-name">
              ${name}
            </div>


            <div>

              <div class="segment-track">

                <div
                  class="segment-current"
                  style="width:${current}%">
                </div>

              </div>


              <div class="segment-track">

                <div
                  class="segment-character"
                  style="width:${character}%">
                </div>

              </div>

            </div>


            <div
              class="
                segment-diff
                ${
                  diff >= 0
                  ? "positive"
                  : "negative"
                }
              "
            >

              ${
                diff >= 0
                ? "+"
                : ""
              }

              ${diff}pt

            </div>

          </div>

          `;

        }
      )
      .join("");

}



init();
