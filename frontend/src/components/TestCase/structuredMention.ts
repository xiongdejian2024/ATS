import {Node,mergeAttributes} from '@tiptap/core'
/** Atomic identity node: display labels never substitute for persisted IDs. */
export const StructuredMention=Node.create({
  name:'structuredMention',group:'inline',inline:true,atom:true,selectable:false,
  addAttributes(){return {
    id:{default:null,parseHTML:el=>el.getAttribute('data-mention-id'),renderHTML:attrs=>({'data-mention-id':attrs.id})},
    label:{default:'',parseHTML:el=>el.getAttribute('data-mention-label')||'',renderHTML:attrs=>({'data-mention-label':attrs.label})},
  }},
  parseHTML(){return [{tag:'span[data-mention-id]'}]},
  renderHTML({HTMLAttributes,node}){return ['span',mergeAttributes(HTMLAttributes,{class:'structured-mention'}),'@'+node.attrs.label]},
  renderText({node}){return '@'+node.attrs.label},
})
