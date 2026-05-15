from stage.postprocessing.xml_parser_refinement import XMLParserRefinement

from lxml import etree

EDOAL_STRING = """<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns="http://knowledgeweb.semanticweb.org/heterogeneity/alignment#" xmlns:alext="http://exmo.inrialpes.fr/align/ext/1.0/" xmlns:align="http://knowledgeweb.semanticweb.org/heterogeneity/alignment#" xmlns:edoal="http://ns.inria.org/edoal/1.0/#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xsd="http://www.w3.org/2001/XMLSchema#">
 <align:Alignment>
  <align:xml>
   yes
  </align:xml>
  <align:level>
   2EDOAL
  </align:level>
  <align:type>
   **
  </align:type>
  <align:onto1>
   <align:Ontology rdf:about="http://cmt#"/>
  </align:onto1>
  <align:onto2>
   <align:Ontology rdf:about="http://confOf#"/>
  </align:onto2>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://cmt#User"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://confOf#Person"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://cmt#Author"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://confOf#Author"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://cmt#Paper"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://confOf#Paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://cmt#Paper"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://confOf#Contribution"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:resource="http://cmt#title"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:resource="http://confOf#hasTitle"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:resource="http://cmt#hasAuthor"/>
    </align:entity1>
    <align:entity2>
     <edoal:inverse>
      <edoal:Relation rdf:resource="http://confOf#writtenBy"/>
     </edoal:inverse>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:resource="http://cmt#abstract"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:resource="http://confOf#abstract"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:resource="http://cmt#hasSubjectArea"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:resource="http://confOf#hasKeyword"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:resource="http://cmt#submitPaper"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:resource="http://confOf#writes"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
 </align:Alignment>
 <align:map>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#ConferenceMember"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Participant"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#ProgramCommitteeMember"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Member_PC"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#Author"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Author"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#Reviewer"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation>
     <edoal:and rdf:parseType="Collection">
      <edoal:RelationDomainRestriction>
       <edoal:class>
        <edoal:Class rdf:about="http://confOf#Member_PC"/>
       </edoal:class>
      </edoal:RelationDomainRestriction>
      <edoal:Relation rdf:about="http://confOf#reviewes"/>
     </edoal:and>
    </edoal:Relation>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://cmt#memberOfConference"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://confOf#expertOn"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://cmt#hasConferenceMember"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation>
     <edoal:inverse>
      <edoal:Relation rdf:about="http://confOf#hasAuthor"/>
     </edoal:inverse>
    </edoal:Relation>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#Reviewer"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Member_PC"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://cmt#readPaper"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://confOf#reviewes"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://cmt#adjustBid"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://confOf#expertOn"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#ProgramCommitteeMember"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Member_PC"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#ConferenceMember"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Member_PC"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#ProgramCommitteeChair"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Chair_PC"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://cmt#memberOfProgramCommittee"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://confOf#expertOn"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://cmt#addProgramCommitteeMember"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://confOf#hasEmail"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    0.7
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#Author"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Author"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://cmt#writePaper"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://confOf#writes"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation>
     <edoal:inverse>
      <edoal:Relation rdf:about="http://confOf#writtenBy"/>
     </edoal:inverse>
    </edoal:Relation>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://cmt#writePaper"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#Co-author"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Author"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://cmt#AuthorNotReviewer"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://confOf#Author"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
</rdf:RDF>
"""

EDOAL_STRING_INCORRECT = """<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns="http://knowledgeweb.semanticweb.org/heterogeneity/alignment#" xmlns:alext="http://exmo.inrialpes.fr/align/ext/1.0/" xmlns:align="http://knowledgeweb.semanticweb.org/heterogeneity/alignment#" xmlns:edoal="http://ns.inria.org/edoal/1.0/#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xsd="http://www.w3.org/2001/XMLSchema#">
 <align:Alignment>
  <align:xml>
   yes
  </align:xml>
  <align:level>
   2EDOAL
  </align:level>
  <align:type>
   **
  </align:type>
  <align:onto1>
   <align:Ontology rdf:about="http://example.org/ontology1/">
    <align:location>
     http://example.org/ontology1/
    </align:location>
    <align:formalism>
     <align:Formalism align:name="owl" align:uri="http://www.w3.org/TR/owl-guide/"/>
    </align:formalism>
   </align:Ontology>
  </align:onto1>
  <align:onto2>
   <align:Ontology rdf:about="http://example.org/ontology2/">
    <align:location>
     http://example.org/ontology2/
    </align:location>
    <align:formalism>
     <align:Formalism align:name="owl" align:uri="http://www.w3.org/TR/owl-guide/"/>
    </align:formalism>
   </align:Ontology>
  </align:onto2>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/chairman"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/conference_chair"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/program_committee_member"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/tpcmember"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/conference_member"/>
    </align:entity1>
    <align:entity2>
     <edoal:inverse>
      <edoal:Relation rdf:about="http://example.org/ontology2/conference_has_member_person"/>
     </edoal:inverse>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/user"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/person"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/has_conflict_of_interest"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/conference_has_member_person"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     0.6
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure>
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/has_conference_member_domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/has_member_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/member_of_conference_range_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/is_member_of_range_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/start_reviewer_bidding_range_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/start_date_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/end_reviewer_bidding_range_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/end_date_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/date_domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/start_date_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/date_domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/end_date_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/site_url_domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/has_name_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/paper_due_on_domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/paper_due_on_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/registration_due_on_domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/registration_due_on_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/manuscript_due_on_domain_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/manuscript_due_on_domain_conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/paper"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/paper_full_version"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/published_paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/paper_abstract"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/pending_paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/has_author"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/paper_is_written_by_author"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation>
      <edoal:inverse>
       <edoal:Relation rdf:about="http://example.org/ontology1/has_author"/>
      </edoal:inverse>
     </edoal:Relation>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/author_has_related_paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/accepted_by"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/accepted_paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/reject_paper"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/rejected_paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/submit_paper"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/pending_paper"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/conference"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/has_conference_member"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/has_member"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:about="http://example.org/ontology1/member_of_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation rdf:about="http://example.org/ontology2/is_member_of"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/conference_member"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/person"/>
    </align:entity2>
    <align:relation>
     &lt;
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/program_committee_member"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/tpcmember"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Class rdf:about="http://example.org/ontology1/conference_chair"/>
    </align:entity1>
    <align:entity2>
     <edoal:Class rdf:about="http://example.org/ontology2/conference_chair"/>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
   <align:Cell>
    <align:entity1>
     <edoal:Relation rdf:resource="http://example.org/ontology1/member_of_conference"/>
    </align:entity1>
    <align:entity2>
     <edoal:Relation>
      <edoal:inverse>
       <edoal:Relation rdf:resource="http://example.org/ontology2/conference_has%20member"/>
      </edoal:inverse>
     </edoal:Relation>
    </align:entity2>
    <align:relation>
     =
    </align:relation>
    <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
     1.0
    </align:measure>
   </align:Cell>
  </align:map>
  <align:map>
  </align:map>
 </align:Alignment>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/program_committee_member"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/tpcmember"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/chairman"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/conference_chair"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/user"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/attendee"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation>
     <edoal:inverse>
      <edoal:Relation rdf:about="http://example.org/ontology1/has_author"/>
     </edoal:inverse>
    </edoal:Relation>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/has_member"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/is_member_of"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/is_member_of"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/author"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/person"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation>
     <edoal:compose rdf:parseType="Collection">
      <edoal:Relation rdf:resource="http://example.org/ontology1/has_conflict_of_interest"/>
     </edoal:compose>
    </edoal:Relation>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/has_biography"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/member_of_conference"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/is_member_of"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/has_conference_member"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/has_member"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/enter_conference_details"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/has_name"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    0.8
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/start_reviewer_bidding"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/start_date"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    0.7
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/end_reviewer_bidding"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/end_date"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    0.7
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/paper_assignment_finalized"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/paper_due_on"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    0.6
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/conference"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/conference"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/review"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/review"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/paper"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/paper"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/written_by"/>
   </align:entity1>
   <align:entity2>
    <edoal:inverse>
     <edoal:Relation rdf:about="http://example.org/ontology2/is_written_by"/>
    </edoal:inverse>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation>
     <edoal:and rdf:parseType="Collection">
      <edoal:RelationDomainRestriction>
       <edoal:class>
        <edoal:Class rdf:about="http://example.org/ontology1/conference"/>
       </edoal:class>
      </edoal:RelationDomainRestriction>
      <edoal:Relation rdf:about="http://example.org/ontology1/has_conference_member"/>
     </edoal:and>
    </edoal:Relation>
   </align:entity1>
   <align:entity2>
    <edoal:Relation>
     <edoal:and rdf:parseType="Collection">
      <edoal:RelationDomainRestriction>
       <edoal:class>
        <edoal:Class rdf:about="http://example.org/ontology2/conference"/>
       </edoal:class>
      </edoal:RelationDomainRestriction>
      <edoal:Relation rdf:about="http://example.org/ontology2/has_member"/>
     </edoal:and>
    </edoal:Relation>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation>
     <edoal:inverse>
      <edoal:Relation rdf:about="http://example.org/ontology1/member_of_conference"/>
     </edoal:inverse>
    </edoal:Relation>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/is_member_of"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology1/author"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology2/author"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/has_co-author"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/is_written_by"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/submit_paper"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/has_related_paper"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation>
     <edoal:inverse>
      <edoal:Relation rdf:about="http://example.org/ontology1/has_author"/>
     </edoal:inverse>
    </edoal:Relation>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/is_written_by"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="http://example.org/ontology1/co-write_paper"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="http://example.org/ontology2/is_written_by"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Class rdf:about="http://example.org/ontology2/presenter"/>
   </align:entity1>
   <align:entity2>
    <edoal:Class rdf:about="http://example.org/ontology1/author"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation>
     <edoal:inverse>
      <edoal:Relation rdf:about="member_of_conference"/>
     </edoal:inverse>
    </edoal:Relation>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="is_member_of"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
 <align:map>
  <align:Cell>
   <align:entity1>
    <edoal:Relation rdf:about="has_conference_member"/>
   </align:entity1>
   <align:entity2>
    <edoal:Relation rdf:about="has member"/>
   </align:entity2>
   <align:relation>
    =
   </align:relation>
   <align:measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">
    1.0
   </align:measure>
  </align:Cell>
 </align:map>
</rdf:RDF>
"""

NS = {
    "align": "http://knowledgeweb.semanticweb.org/heterogeneity/alignment#",
    "edoal": "http://ns.inria.org/edoal/1.0/#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}

SOURCE_CONCEPTS_DICT = {
    "http://cmt#Paper": "paper",
    "http://cmt#Author": "author",
    "http://cmt#hasConferenceMember": "has_conference_member",
    "http://cmt#Conference": "conference",
}

TARGET_CONCEPTS_DICT = {
    "http://edas#Paper": "paper",
    "http://edas#Author": "author",
    "http://edas#hasMember": "has_member",
    "http://edas#isMemberOf": "is_member_of",
    "http://edas#Conference": "conference",
}

def test_parser_edoal_file_author():
    root = XMLParserRefinement(EDOAL_STRING).parse()
    classes = root.xpath("//edoal:Class[@rdf:about='http://cmt#Author']", namespaces=NS)
    assert len(classes) == 3

def test_parser_edoal_file_author_not_reviewer():
    root = XMLParserRefinement(EDOAL_STRING).parse()
    classes = root.xpath("//edoal:Class[@rdf:about='http://cmt#AuthorNotReviewer']", namespaces=NS)
    assert len(classes) == 1

def test_refinement_edoal_file_author_not_reviewer():
    xml_parser = XMLParserRefinement(EDOAL_STRING_INCORRECT)
    root = xml_parser.parse()
    xml_parser.refine(root, SOURCE_CONCEPTS_DICT, "source")
    xml_parser.refine(root, TARGET_CONCEPTS_DICT, "target")
    new_xml_str = etree.tostring(root, pretty_print=True, encoding="unicode")
    assert 'ontology1/paper"' not in new_xml_str
    assert 'rdf:about="http://cmt#Paper"' in new_xml_str and 'rdf:about="http://edas#Paper"' in new_xml_str
    assert 'ontology1/author"' not in new_xml_str
    assert 'rdf:about="http://cmt#Author"' in new_xml_str and 'rdf:about="http://edas#Author"' in new_xml_str
    assert '/has conference member"' not in new_xml_str
    assert 'rdf:about="http://cmt#hasConferenceMember"' in new_xml_str and 'rdf:about="http://cmt#hasConferenceMember"' in new_xml_str
    assert 'ontology1/conference"' not in new_xml_str
    assert 'rdf:about="http://cmt#Conference"' in new_xml_str and 'rdf:about="http://edas#Conference"' in new_xml_str
    assert '/has member"' not in new_xml_str
    assert 'rdf:about="http://edas#hasMember"' in new_xml_str and 'rdf:about="http://edas#hasMember"' in new_xml_str
    assert '/is member of"' not in new_xml_str
    assert 'rdf:about="http://edas#isMemberOf"' in new_xml_str and 'rdf:about="http://edas#isMemberOf"' in new_xml_str