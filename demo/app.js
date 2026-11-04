"use strict";
const data = window.DEMO_DATA;
const $ = id => document.getElementById(id);
const products = [...new Set(data.pair_scores.map(x=>x.product_variable))];
const characters = [...new Set(data.pair_scores.map(x=>x.character_variable))];
function options(id, values){for(const value of values){const option=document.createElement('option');option.value=value;option.textContent=value;$(id).append(option);}}
options('product',products);options('character',characters);
const number = (v, digits=3)=>Number(v).toFixed(digits);
const points = v=>(Number(v)>=0?'+':'')+number(Number(v)*100,2)+' pt';
function rows(){return data.pair_scores.filter(x=>x.product_variable===$('product').value).sort((a,b)=>Number(b[$('sort').value])-Number(a[$('sort').value]) || a.character_variable.localeCompare(b.character_variable));}
function render(){
 const product=$('product').value, character=$('character').value;
 const pair=data.pair_scores.find(x=>x.product_variable===product&&x.character_variable===character);
 $('pair-title').textContent=product+' × '+character;
 $('category').textContent=pair.candidate_type;
 $('compatibility').textContent=number(pair.compatibility_m30);
 $('expansion').textContent=number(pair.expansion_m30);
 $('unexpected').textContent=points(pair.unexpected_affinity);
 $('reason').textContent=pair.recommendation_reason;
 const p=data.product_vectors.find(x=>x.entity_variable===product),c=data.character_vectors.find(x=>x.character_variable===character);
 $('chart').replaceChildren();
 for(let k=1;k<=4;k++){
  const row=document.createElement('div');row.className='cluster';const label=document.createElement('span');label.className='cluster-label';label.textContent='クラスタ '+k;row.append(label);
  const bars=document.createElement('div');bars.className='bars';
  [Number(p['C'+k+'_share']),Number(c['m30_C'+k+'_share'])].forEach((v,i)=>{const line=document.createElement('div');line.className='bar-row';const bar=document.createElement('div');bar.className='bar'+(i?' character':'');bar.style.width=(v*100)+'%';const value=document.createElement('span');value.textContent=number(v*100,1)+'%';line.append(bar,value);bars.append(line);});row.append(bars);$('chart').append(row);
 }
 $('ranking').replaceChildren();
 for(const item of rows()){
  const tr=document.createElement('tr');if(item.character_variable===character)tr.className='selected';
  const td=document.createElement('td'),button=document.createElement('button');button.textContent=item.character_variable;button.setAttribute('aria-label',item.character_variable+'を選択');button.onclick=()=>{$('character').value=item.character_variable;render();};td.append(button);tr.append(td);
  for(const text of [number(item.compatibility_m30),number(item.expansion_m30),points(item.unexpected_affinity),item.candidate_type]){const cell=document.createElement('td');cell.textContent=text;tr.append(cell);}$('ranking').append(tr);
 }
}
for(const id of ['product','character','sort'])$(id).addEventListener('change',render);
$('download').onclick=()=>{const selected=rows(),keys=Object.keys(selected[0]);const escape=v=>'"'+String(v).replaceAll('"','""')+'"';const csv='\ufeff'+[keys,...selected.map(row=>keys.map(k=>row[k]))].map(row=>row.map(escape).join(',')).join('\r\n');const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=$('product').value+'_synthetic_pairs.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
render();
